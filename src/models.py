from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Song:
    title: str
    artists: list[str]
    album: Optional[str] = None
    duration: Optional[str] = None

    @property
    def primary_artist(self) -> Optional[str]:
        return self.artists[0] if self.artists else None