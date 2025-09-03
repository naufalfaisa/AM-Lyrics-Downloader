import sys
from datetime import datetime
from rich.console import Console

class Logger:
    def __init__(self):
        self.__console = Console()

    def _log(self, level: str, color: str, message: str, exit: int = 0):
        now = datetime.now().strftime("%H:%M:%S")
        log = f"[bold yellow][{now}][/] [{color}]{level}:[/] [bold white]{message}[/]"
        self.__console.print(log)
        if exit:
            sys.exit()

    def info(self, message: str, exit: int = 0):
        self._log("INFO", "blue", message, exit)

    def error(self, message: str, exit: int = 0):
        self._log("ERROR", "bold red", message, exit)

    def warning(self, message: str, exit: int = 0):
        self._log("WARNING", "bold yellow", message, exit)

    def done(self, message: str = "Operation completed!."):
        self._log("DONE", "bold green", message)

    def processing_url(self, url: str):
        self.info(f"Processing URL: {url}")

    def failed_fetch(self, url: str, error:Exception):
        self.error(f"Failed to fetch data for URL '{url}': {error}")

    def file_exists(self, filename: str):
        self.warning(f'"{filename}" already exists!')

    def no_lyrics(self, track_name: str):
        self.warning(f'No lyrics for "{track_name}"')

    def no_time_synced(self, track_name: str):
        self.warning(f'No time-synced lyrics for "{track_name}"')

    def no_romaji_lyrics(self, track_name: str):
        self.warning(f'No romaji lyrics for "{track_name}"')

    def no_romaji_time_synced(self, track_name: str):
        self.warning(f'No romaji time-synced lyrics for "{track_name}"')

    def saving_file(self, filename: str):
        self.info(f'Saving "{filename}"...')

logger = Logger()
