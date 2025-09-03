from bs4 import BeautifulSoup

def __getTs(ts: str, syncpoints: int) -> str:
    ts = str(ts).replace("s", "")

    if ":" in ts:
        parts = ts.split(":")
        mins = int(parts[-2])
        secs = float(parts[-1])
    else:
        total_secs = float(ts)
        mins, secs = divmod(total_secs, 60)

    if syncpoints == 3:
        return f"{int(mins):02d}:{secs:06.3f}"
    else:
        return f"{int(mins):02d}:{secs:05.2f}"

def getLyrics(ttml: str, syncpoints: int):
    soup = BeautifulSoup(ttml, "lxml")

    info = {}
    lyrics = []
    timeSyncedLyrics = []

    songwriters = [sw.text for sw in soup.find_all("songwriter")]
    if songwriters:
        info["songwriter"] = ", ".join(songwriters)

    timing = soup.find("tt").get("itunes:timing") if soup.find("tt") else None

    for line in soup.find_all("p"):
        text = line.text.strip()
        if not text:
            continue
        lyrics.append(text)

        if timing and timing != "None":
            spans = line.find_all("span", attrs={"begin": True, "end": True})
            if spans:
                for s in spans:
                    begin = __getTs(s.get("begin"), syncpoints)
                    timeSyncedLyrics.append(f"[{begin}]{s.text}")
            elif line.get("begin"):
                begin = __getTs(line.get("begin"), syncpoints)
                timeSyncedLyrics.append(f"[{begin}]{text}")

    info["lyrics"] = lyrics
    if timeSyncedLyrics:
        info["timeSyncedLyrics"] = timeSyncedLyrics

    return info
