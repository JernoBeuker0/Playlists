from __future__ import annotations

from dataclasses import dataclass

from .models import Song
from .spotify_client import SpotifyClient
from .yt_client import YouTubeMusicClient


@dataclass
class TransferResult:
    playlist_id: str
    source_songs: list[Song]
    matched_songs: list[Song]
    missed_songs: list[Song]


class PlaylistTransferService:
    def __init__(
        self,
        yt_client: YouTubeMusicClient,
        spotify_client: SpotifyClient,
    ) -> None:
        self.yt_client = yt_client
        self.spotify_client = spotify_client

    def transfer_playlist(
        self,
        yt_playlist_id: str,
        spotify_playlist_name: str,
        spotify_playlist_description: str = "",
        public: bool = False,
    ) -> TransferResult:
        songs = self.yt_client.get_playlist_tracks(yt_playlist_id)

        playlist_id = self.spotify_client.create_playlist(
            name=spotify_playlist_name,
            description=spotify_playlist_description,
            public=public,
        )

        matched_songs: list[Song] = []
        missed_songs: list[Song] = []
        track_uris: list[str] = []

        for song in songs:
            uri = self.spotify_client.search_track(song)

            if uri:
                matched_songs.append(song)
                track_uris.append(uri)
            else:
                missed_songs.append(song)

        self.spotify_client.add_tracks_to_playlist(playlist_id, track_uris)

        return TransferResult(
            playlist_id=playlist_id,
            source_songs=songs,
            matched_songs=matched_songs,
            missed_songs=missed_songs,
        )