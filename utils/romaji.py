import re
from pykakasi import kakasi
from api.lyrics import getLyrics

class Romaji:
    def __init__(self):
        self.kakasi_obj = kakasi()
        self.kakasi_obj.setMode("H", "a")
        self.kakasi_obj.setMode("K", "a")
        self.kakasi_obj.setMode("J", "a")
        self.kakasi_obj.setMode("r", "Hepburn")
        self.kakasi_obj.setMode("s", True)
        self.conv = self.kakasi_obj.getConverter()

    def clean_romaji(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\bha\b', 'wa', text)
        text = re.sub(r'\bwo\b', 'o', text)
        text = re.sub(r'\bhe\b', 'e', text)
        text = re.sub(r'\(\s*(.*?)\s*\)', r'(\1)', text)
        text = text.strip()
        if text:
            text = text[0].upper() + text[1:]
        return text

    def to_romaji(self, text: str) -> str:
        romaji = self.conv.do(text).strip()
        return self.clean_romaji(romaji)

    def convert_to_romaji(self, lines):
        romaji_lines = []
        for line in lines:
            if line.startswith("[") and "]" in line:
                timestamp, text = line.split("]", 1)
                romaji_lines.append(f"{timestamp}]{self.to_romaji(text)}")
            else:
                romaji_lines.append(self.to_romaji(line))
        return romaji_lines

    def process_lyrics(self, lyrics_data, syncpoints, romaji=False):
        ttml = lyrics_data[0]["attributes"].get("ttml")
        lyrics_info = getLyrics(ttml, syncpoints) or {}
        if romaji and lyrics_info:
            if "lyrics" in lyrics_info:
                lyrics_info["lyrics_romaji"] = [self.to_romaji(line) for line in lyrics_info["lyrics"]]
            if "timeSyncedLyrics" in lyrics_info:
                lyrics_info["timeSyncedLyrics_romaji"] = self.convert_to_romaji(lyrics_info["timeSyncedLyrics"])
        return ttml, lyrics_info
