"""Hexagonal prism solid geometry."""

from __future__ import annotations

from dataclasses import dataclass

from .point import Point3D
from .regular_hexagon import RegularHexagon


@dataclass(frozen=True)
class HexagonalPrism:
    center: Point3D
    radius: float
    height: float

    @property
    def bottom(self) -> RegularHexagon:
        return RegularHexagon(self.center, self.radius)

    @property
    def top(self) -> RegularHexagon:
        return RegularHexagon(self.center.translate(dz=self.height), self.radius)

    def vertices(self):
        return self.bottom.polygon().vertices + self.top.polygon().vertices
