from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Optional

import requests

from .models import Song
from .spotify_auth import SpotifyAuthClient


class SpotifyApiError(RuntimeError):
    pass


class SpotifyClient:
    def __init__(
        self,
        auth: SpotifyAuthClient,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.auth = auth
        self.session = session or requests.Session()
        self.base_url = "https://api.spotify.com/v1"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.auth.get_access_token()}",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        response = self.session.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            json=json,
            timeout=30,
        )

        if not response.ok:
            raise SpotifyApiError(
                f"Spotify API request failed: {response.status_code} {response.text}"
            )

        if response.status_code == 204:
            return None

        return response.json()

    def create_playlist(
        self,
        name: str,
        description: str = "",
        public: bool = False,
    ) -> str:
        payload = {
            "name": name,
            "description": description,
            "public": public,
        }

        data = self._request("POST", "/me/playlists", json=payload)
        return data["id"]

    def search_track(self, song: Song) -> Optional[str]:
        if song.primary_artist:
            query = f'track:{song.title} artist:{song.primary_artist}'
        else:
            query = song.title

        params = {
            "q": query,
            "type": "track",
            "limit": 1,
        }

        data = self._request("GET", "/search", params=params)
        items = data.get("tracks", {}).get("items", [])

        if not items:
            return None

        return items[0]["uri"]

    def add_tracks_to_playlist(
        self,
        playlist_id: str,
        track_uris: Sequence[str],
    ) -> None:
        if not track_uris:
            return

        for i in range(0, len(track_uris), 100):
            batch = list(track_uris[i:i + 100])
            self._request(
                "POST",
                f"/playlists/{playlist_id}/items",
                json={"uris": batch},
            )