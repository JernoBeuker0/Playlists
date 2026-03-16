import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="Transfer a YouTube Music playlist to Spotify.",
    )

    parser.add_argument(
        "playlist_id",
        help="YouTube Music playlist ID",
    )

    parser.add_argument(
        "new_playlist_name",
        help="Name for the new Spotify playlist",
    )

    parser.add_argument(
        "-d",
        "--description",
        default="Imported with Python from YouTube Music",
        help="Optional description for the new Spotify playlist",
    )

    parser.add_argument(
        "-p",
        "--print-songs",
        action="store_true",
        help="Print all songs from the YouTube Music playlist before transferring",
    )

    return parser