import os
import sys
from sanitize_filename import sanitize

from api import AppleMusic
from utils import logger

BASE_PATH = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

def path_in_base(*parts):
    return os.path.join(BASE_PATH, *parts)

CACHE = path_in_base("cache")
CONFIG = path_in_base("config")
LYRICS_FOLDER = path_in_base("lyrics-downloaded")
os.makedirs(LYRICS_FOLDER, exist_ok=True)

def __sanitize(path):
    return sanitize(path) if path else path

def save_lyrics(track, key, directory, suffix, log_exists, log_save, log_missing):
    filename = f"{__sanitize(track.get('file', 'Unknown Track'))}{suffix}"
    path = os.path.join(directory, filename)

    if os.path.exists(path):
        log_exists(filename)
        return False
    elif track.get(key):
        log_save(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(track[key]))
        return True
    else:
        log_missing(track.get("file", "Unknown Track"))
        return False

SAVE_RULES = {
    "lrc": ("timeSyncedLyrics", ".lrc", logger.no_time_synced),
    "txt": ("lyrics", ".txt", logger.no_lyrics),
    "lrc_romaji": ("timeSyncedLyrics_romaji", ".lrc", logger.no_romaji_time_synced),
    "txt_romaji": ("lyrics_romaji", ".txt", logger.no_romaji_lyrics),
}

def process_track(track, rules, dirs):
    saved, skipped = 0, 0
    for key, (lyric_key, ext, log_missing) in rules.items():
        if key in dirs:
            if save_lyrics(track, lyric_key, dirs[key], ext,
                           logger.file_exists, logger.saving_file, log_missing):
                saved += 1
            else:
                skipped += 1
    return saved, skipped

def downloader(args, mode="lrc"):
    syncMsPointCount = 3 if args.sync else 2
    applemusic = AppleMusic(CACHE, CONFIG, syncMsPointCount)

    save_romaji, save_txt, save_txt_only = getattr(args, "romaji", False), getattr(args, "txt", False), getattr(args, "txt_only", False)

    active = {}
    if save_romaji:
        if save_txt_only:
            active["txt_romaji"] = True
        elif save_txt:
            active.update({"txt_romaji": True, "lrc_romaji": True})
        else:
            active["lrc_romaji"] = True
    else:
        if save_txt_only:
            active["txt"] = True
        elif save_txt:
            active.update({"txt": True, "lrc": True})
        else:
            active["lrc"] = True

    for url in args.urls:
        logger.processing_url(url)
        try:
            data = applemusic.getInfo(url, romaji=save_romaji)
        except Exception as e:
            logger.failed_fetch(url, e)
            continue

        album_dir = __sanitize(data.get("dir", "Unknown Album"))

        dirs = {}
        if "lrc" in active or "txt" in active:
            base_dir = os.path.join(LYRICS_FOLDER, album_dir)
            os.makedirs(base_dir, exist_ok=True)
            if "lrc" in active: dirs["lrc"] = base_dir
            if "txt" in active: dirs["txt"] = base_dir

        if "lrc_romaji" in active or "txt_romaji" in active:
            romaji_dir = os.path.join(LYRICS_FOLDER, f"(Romaji) {album_dir}")
            os.makedirs(romaji_dir, exist_ok=True)
            if "lrc_romaji" in active: dirs["lrc_romaji"] = romaji_dir
            if "txt_romaji" in active: dirs["txt_romaji"] = romaji_dir

        saved_total, skipped_total = 0, 0
        for track in data.get("tracks", []):
            saved, skipped = process_track(track, SAVE_RULES, dirs)
            saved_total += saved
            skipped_total += skipped

        logger.done(f'Album "{album_dir}": {saved_total} files saved, {skipped_total} files skipped')
