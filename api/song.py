from utils import Romaji

romaji_converter = Romaji()

def song(data, syncpoints, romaji=False):
    info = {}
    attr = data["data"][0]["relationships"]["albums"]["data"][0]["attributes"]
    name = attr["name"]

    replacements = {" - EP": " [EP]", " - Single": " [Single]"}
    for key, val in replacements.items():
        if key in name:
            name = name.replace(key, "") + val

    info["dir"] = f"{attr['artistName']} - {name}"
    trackList = []

    for track in data["data"]:
        __info = {}
        track_attr = track["attributes"]
        track_number = track_attr.get("trackNumber")
        track_name = track_attr.get("name")

        __info["file"] = f"{str(track_number).zfill(2)}. {track_name}"

        lyrics_data = track.get("relationships", {}).get("lyrics", {}).get("data", [])
        if lyrics_data:
            ttml, lyrics_info = romaji_converter.process_lyrics(lyrics_data, syncpoints, romaji)
            __info["ttml"] = ttml
            __info.update(lyrics_info or {})

        trackList.append(__info)

    info["tracks"] = trackList
    return info
