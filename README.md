# Apple Music Lyrics Downloader

A python program to fetch lyrics with timestamp from apple music albums and songs.

## Required

Apple Music media user token (requires an active subscription)

## Installation (Python)

Clone the repository and install dependencies:

```
git clone https://github.com/naufalfaisa/AM-Lyrics-Downloader.git
cd AM-Lyrics-Downloader

pip install -r requirements.txt
```
Run the program:

```
python main.py [options] <urls...>
```

## Usage (Windows .exe)

Download the .exe from the [releases](https://github.com/naufalfaisa/AM-Lyrics-Downloader) and run:

```
main.exe [options] <urls...>
```

## Options

| Options | Description |
| --- | --- |
| `-h`, `--help` | Show this help message and exit|
| `-v`, `--version` | Show program version (optional)|
| `-s`, `--sync` | Save timecodes in `00:00.000` (three ms points)|
| `--txt` | Save the `.txt` file lyrics (no timestamp)|
| `--txt-only` | Save lyrics only in `.txt` file (no timestamp)|

## Example

```
# Download lyrics in default .lrc format
main.exe https://music.apple.com/album/...

# Download lyrics in .txt format alongside .lrc
main.exe --txt https://music.apple.com/album/...

# Download only .txt lyrics
main.exe --txt-only https://music.apple.com/album/...

# Save timecodes in `00:00.000` (three ms points)
main.exe -s https://music.apple.com/album/...
```

## Output

Downloads are saved in:

```
./lyrics-downloaded/
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credit

This project is based on and modified from [Manzana-Apple-Music-Lyrics](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics) by [dropcreations](https://github.com/dropcreations).
