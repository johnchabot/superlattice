"""Face primitive for solid topology."""

from __future__ import annotations

from dataclasses import dataclass

from .polygon import Polygon


@dataclass(frozen=True)
class Face:
    polygon: Polygon
    name: str = ""
