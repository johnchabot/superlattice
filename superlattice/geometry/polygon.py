"""Polygon primitives built from Point3D vertices."""

from __future__ import annotations

from dataclasses import dataclass
from .point import Point3D


@dataclass(frozen=True)
class Polygon:
    """Immutable ordered polygon."""

    vertices: tuple[Point3D, ...]

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def is_closed(self) -> bool:
        return self.vertex_count >= 3
