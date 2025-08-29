import argparse
from rich.console import Console
from rich.traceback import install

from handler import arguments

install()
console = Console()

LOGO = r"""
[bright_white bold]⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕
⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂
⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂
⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔
⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿
⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣷⣵⣵⣵⣷⣿⣿⣿⣿⣿⣿⡿
⢌⠻⣿⡿⡫⡪⡪⡪⡪⣺⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠣⡁⠹⡪⡪⡪⡪⣪⣾⣿⣿⣿⣿⠋⠐⢉⢍⢄⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈
⡣⡘⢄⠙⣾⣾⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⡘⣿⣿⣿⣿⣿⣿⠏⠠⠈
⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⣿⣿⣿⣿⡿⢋⢜⠠⠈
──── Apple Music Lyrics ────[/]
"""

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v1.0.0'
    )
    parser.add_argument(
        '-s', '--sync',
        help="Save timecode's in 00:00.000 format (three ms points)",
        action="store_true"
    )
    parser.add_argument(
        '--txt',
        help="Save lyrics as .txt (along with .lrc if available)",
        action="store_true"
    )
    parser.add_argument(
        '--txt-only',
        help="Save only .txt, do not save .lrc",
        action="store_true"
    )
    parser.add_argument(
        'urls',
        help="Apple Music URL for an album or a song",
        type=str,
        nargs='*'
    )
    return parser

def detect_mode(args) -> str:
    if args.txt:
        return "txt"
    if args.txt_only:
        return "txt_only"
    return "lrc"

def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if not args.urls:
            url = input("Input Apple Music album or a song URL: ").strip()
            if not url:
                console.print("[red]No URL provided, exiting...[/]")
                return
            args.urls = [url]

        mode = detect_mode(args)
        arguments(args, mode)

    except KeyboardInterrupt:
        console.print("\n[yellow]Aborted by user (Ctrl+C).[/]")

if __name__ == "__main__":
    console.print(LOGO)
    main()
    input("\nPress Enter to exit...")
