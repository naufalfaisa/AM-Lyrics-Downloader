from api.lyrics import getLyrics

def album(data, syncpoints):
    info = {}
    attr = data["data"][0]["attributes"]

    name = attr["name"]

    if " - EP" in name:
        name = name.replace(" - EP", "") + " [EP]"
    if " - Single" in name:
        name = name.replace(" - Single", "") + " [Single]"

    __dir = f"{attr['artistName']} - {name}"
    info["dir"] = __dir

    trackList = []
    tracks = data["data"][0]["relationships"]["tracks"]["data"]

    for track in tracks:
        __info = {}
        attr = track["attributes"]

        if track.get("type") == "songs":
            track_number = attr.get('trackNumber')
            track_name = attr.get('name')
            __file = f"{str(track_number).zfill(2)}. {track_name}"
            __info["file"] = __file

            lyrics_data = track.get("relationships", {}).get("lyrics", {}).get("data", [])
            if lyrics_data:
                ttml = lyrics_data[0]["attributes"].get("ttml")
                __info["ttml"] = ttml
                __info.update(getLyrics(ttml, syncpoints))

        trackList.append(__info)

    info["tracks"] = trackList
    return info
