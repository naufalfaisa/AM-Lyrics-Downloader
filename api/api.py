import re
import requests

from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from utils import Cache
from utils import logger
from config import Configure

from api.album import album
from api.song import song

HEADERS = {
    'content-type': 'application/json;charset=utf-8',
    'connection': 'keep-alive',
    'accept': 'application/json',
    'origin': 'https://music.apple.com',
    'referer': 'https://music.apple.com/',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

class AppleMusic(object):
    def __init__(self, cache: str, config: str, sync: int):
        self.__session = requests.Session()
        self.__session.headers = HEADERS

        self.__cache = Cache(cache)
        self.__config = Configure(config)

        self.sync = sync

        self.__accessToken()
        self.__mediaUserToken()

    def __checkUrl(self, url):
        try:
            urlopen(url)
            return True
        except (URLError, HTTPError) as e:
            logger.error(f"URL check failed: {e}", 1)
            return False

    def __getUrl(self, url):
        __url = urlparse(url)
        if not __url.scheme:
            url = f"https://{url}"

        if __url.netloc == "music.apple.com":
            if self.__checkUrl(url):
                splits = url.split('/')
                id = splits[-1]
                kind = splits[4]

                if kind == "album" and '?i=' in id:
                    id = id.split('?i=')[1]
                    kind = "song"

                self.kind = kind
                self.id = id
            else:
                logger.error("URL is invalid!", 1)
        else:
            logger.error("URL is invalid!", 1)

    def __accessToken(self):
        accessToken = self.__cache.get("accessToken")

        if not accessToken:
            logger.info("Fetching access token from web...")
            try:
                response = requests.get('https://music.apple.com/us/browse')
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Failed to get music.apple.com: {e}", 1)
                return

            try:
                indexJs = re.search(r'(?<=index)(.*?)(?=\.js")', response.text).group(1)
            except AttributeError:
                logger.error("Failed to parse index.js URL from Apple Music page", 1)
                return

            try:
                response_js = requests.get(f'https://music.apple.com/assets/index{indexJs}.js')
                response_js.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Failed to get js library: {e}", 1)
                return

            try:
                accessToken = re.search(r'(?=eyJh)(.*?)(?=")', response_js.text).group(1)
            except AttributeError:
                logger.error("Failed to parse access token from js library", 1)
                return

            self.__cache.set("accessToken", accessToken)
        else:
            logger.info("Checking access token found in cache...")

        self.__session.headers.update({'authorization': f'Bearer {accessToken}'})

        try:
            response = self.__session.get("https://amp-api.music.apple.com/v1/catalog/us/songs/1450330685")
            if not response.text:
                logger.info("Access token in cache is expired, refreshing...")
                self.__cache.delete("accessToken")
                self.__accessToken()
        except requests.RequestException as e:
            logger.error(f"Error checking access token: {e}", 1)

    def __mediaUserToken(self, fromLoop=False):
        token = self.__config.get()
        if token:
            logger.info("Checking media-user-token...")
            self.__session.headers.update({"media-user-token": token})
            try:
                response = self.__session.get("https://amp-api.music.apple.com/v1/me/storefront")
                response.raise_for_status()
                data = response.json()
                self.storefront = data["data"][0].get("id")
                self.language = data["data"][0]["attributes"].get("defaultLanguageTag")
                self.__session.headers.update({'accept-language': f'{self.language},en;q=0.9'})
            except requests.RequestException as e:
                logger.error(f"Invalid media-user-token: {e}", 1)
                self.__config.delete()
                self.__config.set()
                self.__mediaUserToken(fromLoop=True)
            except (KeyError, IndexError, ValueError) as e:
                logger.error(f"Failed to parse media-user-token response: {e}", 1)
        else:
            if not fromLoop:
                logger.error("Enter your media-user-token to continue!", 1)
                self.__config.set()
            logger.info("Re-start the program...", 1)

    def __getErrors(self, errors):
        if not isinstance(errors, list):
            errors = [errors]
        for error in errors:
            if isinstance(error, dict):
                err_status = error.get("status", "No status")
                err_detail = error.get("detail", str(error))
            else:
                err_status = "Unknown error type"
                err_detail = str(error)
            logger.error(f"{err_status} - {err_detail}", 1)

    def __getJson(self):
        logger.info("Fetching API response...")
        cacheKey = f"{self.id}:{self.storefront}"
        cached = self.__cache.get(cacheKey)
        if cached:
            logger.info("Using cached response...")
            return cached

        apiUrl = f'https://amp-api.music.apple.com/v1/catalog/{self.storefront}/{self.kind}s/{self.id}'
        self.__session.params = {'include[songs]': 'albums,lyrics,syllable-lyrics', 'l': f'{self.language}'}

        try:
            response = self.__session.get(apiUrl)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch API: {e}", 1)
            return
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}", 1)
            return

        if "errors" not in data:
            self.__cache.set(cacheKey, data)
            return data
        else:
            self.__getErrors(data.get("errors"))

    def getInfo(self, url, romaji=False):
        self.__getUrl(url)
        if self.kind == "album":
            return album(self.__getJson(), syncpoints=self.sync, romaji=romaji)
        elif self.kind == "song":
            return song(self.__getJson(), syncpoints=self.sync, romaji=romaji)
        else:
            logger.error("Supports only albums and songs!", 1)
