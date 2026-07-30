"""Core geometric primitives."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point3D:
    """Immutable 3D point/vector."""

    x: float
    y: float
    z: float

    def translate(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> "Point3D":
        return Point3D(self.x + dx, self.y + dy, self.z + dz)

    def distance_to(self, other: "Point3D") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )
