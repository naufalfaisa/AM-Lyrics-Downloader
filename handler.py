import os
import sys
from sanitize_filename import sanitize

from api import AppleMusic
from utils import logger

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

CACHE = os.path.join(__get_path(), "cache")
CONFIG = os.path.join(__get_path(), "config")

LYRICS_FOLDER = os.path.join(__get_path(), "lyrics-downloaded")
if not os.path.exists(LYRICS_FOLDER):
    os.makedirs(LYRICS_FOLDER)

def __sanitize(path):
    return sanitize(path) if path else path

def arguments(args, mode="lrc"):
    """
    mode: "lrc" (default), "txt" (txt + lrc), "txt_only" (txt only)
    """
    syncMsPointCount = 3 if args.sync else 2
    applemusic = AppleMusic(CACHE, CONFIG, syncMsPointCount)

    save_txt = mode in ("txt", "txt_only")
    save_lrc = mode in ("lrc", "txt")

    for url in args.urls:
        try:
            data = applemusic.getInfo(url)
        except Exception as e:
            logger.error(f"Failed to fetch data for URL '{url}': {e}")
            continue

        album_dir = __sanitize(data.get("dir", "Unknown Album"))
        __dir = os.path.join(LYRICS_FOLDER, album_dir)
        os.makedirs(__dir, exist_ok=True)

        for track in data.get("tracks", []):
            track_name = track.get("file", "Unknown Track")

            if save_lrc:
                path_lrc = os.path.join(__dir, f"{__sanitize(track_name)}.lrc")
                if os.path.exists(path_lrc):
                    logger.warning(f'"{track_name}.lrc" already exists!')
                elif track.get("timeSyncedLyrics"):
                    logger.info(f'Saving "{track_name}.lrc"...')
                    with open(path_lrc, "w", encoding="utf-8") as f:
                        f.write("\n".join(track["timeSyncedLyrics"]))
                else:
                    logger.warning(f'No time-synced lyrics for "{track_name}"')

            if save_txt:
                path_txt = os.path.join(__dir, f"{__sanitize(track_name)}.txt")
                if os.path.exists(path_txt):
                    logger.warning(f'"{track_name}.txt" already exists!')
                elif track.get("lyrics"):
                    logger.info(f'Saving "{track_name}.txt"...')
                    with open(path_txt, "w", encoding="utf-8") as f:
                        f.write("\n".join(track["lyrics"]))
                else:
                    logger.warning(f'No lyrics for "{track_name}"')

    logger.info("All done!")
