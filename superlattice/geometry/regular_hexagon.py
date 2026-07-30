"""Canonical regular hexagon geometry."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, pi

from .point import Point3D
from .polygon import Polygon


@dataclass(frozen=True)
class RegularHexagon:
    center: Point3D
    radius: float

    def polygon(self) -> Polygon:
        vertices = tuple(
            Point3D(
                self.center.x + self.radius * cos(i * pi / 3),
                self.center.y + self.radius * sin(i * pi / 3),
                self.center.z,
            )
            for i in range(6)
        )
        return Polygon(vertices)
