from __future__ import annotations

from typing import Optional

from ytmusicapi import YTMusic

from .models import Song


class YouTubeMusicClient:
    def __init__(self, ytmusic: Optional[YTMusic] = None) -> None:
        self.ytmusic = ytmusic or YTMusic()

    def get_playlist_tracks(self, playlist_id: str) -> list[Song]:
        playlist = self.ytmusic.get_playlist(playlist_id, limit=None)
        tracks = playlist.get("tracks", [])

        songs: list[Song] = []

        for track in tracks:
            album_data = track.get("album")
            album_name = (
                album_data.get("name")
                if isinstance(album_data, dict)
                else album_data
            )

            songs.append(
                Song(
                    title=track.get("title", ""),
                    artists=[a["name"] for a in track.get("artists", [])],
                    album=album_name,
                    duration=track.get("duration"),
                )
            )

        return songs