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
    rotation: float = 0.0

    def polygon(self) -> Polygon:
        vertices = []

        for i in range(6):
            angle = self.rotation * pi / 180 + i * pi / 3

            vertices.append(
                Point3D(
                    self.center.x + self.radius * cos(angle),
                    self.center.y + self.radius * sin(angle),
                    self.center.z,
                )
            )

        return Polygon(tuple(vertices))