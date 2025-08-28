# Apple Music Lyrics Downloader

A python program to fetch lyrics with timestamp from apple music albums and songs.

## Required

Apple Music media user token (requires an active subscription)

## Usage

<!-- Clone this repository or download the `.exe` file from the [releases](https://github.com/naufalfaisa/AM-Lyrics-Downloader). -->

```
git clone https://github.com/naufalfaisa/AM-Lyrics-Downloader.git && cd AM-Lyrics-Downloader

pip install -r requirements.txt

python main.py [options] <url>
```

Lyrics are saved in `.lrc` format by default with a timestamp.

## Options

| Arguments | Description |
| --- | --- |
| `-h`, `--help` | Show this help message and exit|
| `-v`, `--version` | Show program version (optional)|
| `-s`, `--sync` | Save timecodes in `00:00.000` (three ms points)|
| `--txt` | Save the `.txt` file lyrics (no timestamp)|
| `--txt-only` | Save lyrics only in `.txt` file (no timestamp)|

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credit

This project is based on and modified from [Manzana-Apple-Music-Lyrics](https://github.com/dropcreations/Manzana-Apple-Music-Lyrics) by [dropcreations](https://github.com/dropcreations).
