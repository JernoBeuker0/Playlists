from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class SpotifySettings:
    client_id: str
    client_secret: str
    refresh_token: str
    token_url: str = "https://accounts.spotify.com/api/token"
    refresh_buffer_seconds: int = 60

    @classmethod
    def from_env(cls) -> "SpotifySettings":
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        missing = [
            name
            for name, value in {
                "SPOTIFY_CLIENT_ID": client_id,
                "SPOTIFY_CLIENT_SECRET": client_secret,
                "SPOTIFY_REFRESH_TOKEN": refresh_token,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )


@dataclass
class SpotifyToken:
    access_token: str
    token_type: str
    expires_at: float
    refresh_token: str
    scope: Optional[str] = None

    def is_expired(self, buffer_seconds: int = 60) -> bool:
        return time.time() >= (self.expires_at - buffer_seconds)


class JsonTokenStore:
    def __init__(self, path: str = ".spotify_token_cache.json") -> None:
        self.path = Path(path)

    def load(self) -> Optional[SpotifyToken]:
        if not self.path.exists():
            return None

        data = json.loads(self.path.read_text(encoding="utf-8"))
        return SpotifyToken(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_at=data["expires_at"],
            refresh_token=data["refresh_token"],
            scope=data.get("scope"),
        )

    def save(self, token: SpotifyToken) -> None:
        payload = {
            "access_token": token.access_token,
            "token_type": token.token_type,
            "expires_at": token.expires_at,
            "refresh_token": token.refresh_token,
            "scope": token.scope,
        }
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class SpotifyAuthError(RuntimeError):
    pass


class SpotifyAuthClient:
    def __init__(
        self,
        settings: SpotifySettings,
        token_store: Optional[JsonTokenStore] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.settings = settings
        self.token_store = token_store or JsonTokenStore()
        self.session = session or requests.Session()

    def get_access_token(self) -> str:
        cached = self.token_store.load()

        if cached and not cached.is_expired(self.settings.refresh_buffer_seconds):
            return cached.access_token

        refresh_token = cached.refresh_token if cached else self.settings.refresh_token
        new_token = self.refresh_access_token(refresh_token)
        self.token_store.save(new_token)
        return new_token.access_token

    def refresh_access_token(self, refresh_token: str) -> SpotifyToken:
        credentials = f"{self.settings.client_id}:{self.settings.client_secret}"
        basic_auth = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = self.session.post(
            self.settings.token_url,
            headers=headers,
            data=data,
            timeout=30,
        )

        if not response.ok:
            raise SpotifyAuthError(
                f"Failed to refresh Spotify token: "
                f"{response.status_code} {response.text}"
            )

        payload = response.json()

        return SpotifyToken(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_at=time.time() + int(payload["expires_in"]),
            refresh_token=payload.get("refresh_token", refresh_token),
            scope=payload.get("scope"),
        )