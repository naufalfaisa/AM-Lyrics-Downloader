from sanitize_filename import sanitize
from utils import Romaji

romaji_converter = Romaji()

def album(data, syncpoints, romaji=False):
    info = {}
    attr = data["data"][0]["attributes"]
    name = attr["name"]

    replacements = {" - EP": " [EP]", " - Single": " [Single]"}
    for key, val in replacements.items():
        if key in name:
            name = name.replace(key, "") + val

    info["dir"] = sanitize(f"{attr['artistName']} - {name}")

    trackList = []
    tracks = data["data"][0].get("relationships", {}).get("tracks", {}).get("data", [])

    for track in tracks:
        __info = {}
        attr = track.get("attributes", {})

        if track.get("type") == "songs":
            track_number = attr.get("trackNumber")
            track_name = attr.get("name", "Unknown")
            __info["file"] = sanitize(f"{str(track_number).zfill(2)}. {track_name}")

            lyrics_data = track.get("relationships", {}).get("lyrics", {}).get("data", [])
            if lyrics_data:
                ttml, lyrics_info = romaji_converter.process_lyrics(lyrics_data, syncpoints, romaji)
                __info["ttml"] = ttml
                __info.update(lyrics_info or {})

        trackList.append(__info)

    info["tracks"] = trackList
    return info
