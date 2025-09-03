# Apple Music Lyrics Downloader

A Python program to fetch lyrics with timestamp from Apple Music albums and songs.

## Features

* Download `.lrc` file (with timestamp) or `.txt` file (without timestamp).
* Save timecodes in `00:00.000` (three ms points).
* Convert Japanese lyrics to Romaji.

## Requirements

Apple Music media user token (requires active subscription) will be asked the first time you run the program.

## Installation (Python)

Clone the repository and install dependencies:

```bash
git clone https://github.com/naufalfaisa/AM-lyrics-downloader.git
cd AM-Lyrics-Downloader
pip install -r requirements.txt
```

Run the program:

```bash
python main.py [options] <urls...>
```

---

## Usage (Windows `.exe`)

Download the `.exe` from the [releases](https://github.com/naufalfaisa/AM-lyrics-downloader/releases) and run:

```bash
main.exe
```

or with options:

```bash
main.exe [options] <urls...>
```

### Interactive Mode

If you run without URLs or options, the program will ask for input:

```
───── Apple Music Lyrics ─────

Enter Apple Music album or song URL: https://music.apple.com/album/...

Enter additional options (comma separated, e.g., txt,txt-only,romaji,sync): romaji,sync
```

---

## Options

| Option            | Description                                         |
| ----------------- | --------------------------------------------------- |
| `-h`, `--help`    | Show this help message and exit                     |
| `-v`, `--version` | Show program version (optional)                     |
| `-s`, `--sync`    | Save timecodes in `00:00.000` (three ms points)     |
| `--txt`           | Save the `.txt` file lyrics (without timestamp)     |
| `--txt-only`      | Save lyrics only in `.txt` file (without timestamp) |
| `--romaji`        | Convert Japanese text to Romaji                     |

---

## Output

Downloads are saved in:

```
./lyrics-downloaded/
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Credit

This project is based on and modified from [Manzana-Apple-Music-Lyrics](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics) by [dropcreations](https://github.com/dropcreations).
