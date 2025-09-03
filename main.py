import argparse
from handler import downloader
import sys

ASCII_BANNER = r"""
⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕
⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂
⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂
⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔
⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿
⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣷⣵⣵⣵⣷⣿⣿⣿⣿⣿⣿⡿
⢌⠻⣿⡿⡫⡪⡪⡪⡪⣺⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠣⡁⠹⡪⡪⡪⡪⣪⣾⣿⣿⣿⣿⠋⠐⢉⢍⢄⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈
⡣⡘⢄⠙⣾⣾⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⡘⣿⣿⣿⣿⣿⣿⠏⠠⠈
⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⣿⣿⣿⣿⡿⢋⢜⠠⠈
"""

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=ASCII_BANNER,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0.0')
    parser.add_argument('-s', '--sync', help="Save timecode's in 00:00.000 format", action="store_true")
    parser.add_argument('--txt', help="Save lyrics as .txt (along with .lrc if available)", action="store_true")
    parser.add_argument('--txt-only', help="Save only .txt, do not save .lrc", action="store_true")
    parser.add_argument('--romaji', help="Save lyrics in Romaji", action="store_true")
    parser.add_argument('urls', help="Apple Music URL for an album or song", type=str, nargs='*')
    return parser

def detect_mode(args) -> str:
    if args.txt:
        return "txt"
    if args.txt_only:
        return "txt_only"
    return "lrc"

def prompt_options_comma():
    options_input = input("\nEnter additional options (comma separated, e.g., txt,txt-only,romaji,sync): ").strip().lower()
    options_list = [opt.strip() for opt in options_input.split(",")] if options_input else []
    return "sync" in options_list, "txt" in options_list, "txt-only" in options_list, "romaji" in options_list

def main():
    print("\n───── Apple Music Lyrics ─────\n")

    parser = build_parser()
    args = parser.parse_args()

    try:
        if not args.urls:
            url = input("Enter Apple Music album or song URL: ").strip()
            if not url:
                print("No URL provided, exiting...")
                return
            args.urls = [url]
            args.sync, args.txt, args.txt_only, args.romaji = prompt_options_comma()

        mode = detect_mode(args)
        downloader(args, mode)

    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
