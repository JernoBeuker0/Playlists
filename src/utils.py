from __future__ import annotations

from collections.abc import Iterable

from .models import Song


def print_songs(songs: Iterable[Song]) -> None:
    """Print songs by title and artist."""
    for song in songs:
        print(f"{song.title} - {', '.join(song.artists)}")