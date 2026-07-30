"""Edge primitive connecting two vertices."""

from __future__ import annotations

from dataclasses import dataclass
from .point import Point3D

@dataclass(frozen=True)
class Edge:
    start: Point3D
    end: Point3D
