"""Hexagonal prism solid geometry."""

from __future__ import annotations

from dataclasses import dataclass

from .edge import Edge
from .face import Face
from .point import Point3D
from .polygon import Polygon
from .regular_hexagon import RegularHexagon
from .solid import Solid


@dataclass(frozen=True)
class HexagonalPrism(Solid):
    center: Point3D
    radius: float
    height: float
    rotation: float = 0.0

    @property
    def bottom(self) -> RegularHexagon:
        return RegularHexagon(
            self.center,
            self.radius,
            self.rotation,
        )

    @property
    def top(self) -> RegularHexagon:
        return RegularHexagon(
            self.center.translate(dz=self.height),
            self.radius,
            self.rotation,
        )

    @property
    def vertices(self) -> tuple[Point3D, ...]:
        return (
            self.bottom.polygon().vertices
            + self.top.polygon().vertices
        )

    @property
    def edges(self) -> tuple[Edge, ...]:
        v = self.vertices

        return (
            # Bottom ring
            Edge(v[0], v[1]),
            Edge(v[1], v[2]),
            Edge(v[2], v[3]),
            Edge(v[3], v[4]),
            Edge(v[4], v[5]),
            Edge(v[5], v[0]),

            # Top ring
            Edge(v[6], v[7]),
            Edge(v[7], v[8]),
            Edge(v[8], v[9]),
            Edge(v[9], v[10]),
            Edge(v[10], v[11]),
            Edge(v[11], v[6]),

            # Vertical edges
            Edge(v[0], v[6]),
            Edge(v[1], v[7]),
            Edge(v[2], v[8]),
            Edge(v[3], v[9]),
            Edge(v[4], v[10]),
            Edge(v[5], v[11]),
        )

    @property
    def faces(self) -> tuple[Face, ...]:
        v = self.vertices

        return (
            Face(
                Polygon((v[6], v[7], v[8], v[9], v[10], v[11])),
                "top",
            ),
            Face(
                Polygon((v[5], v[4], v[3], v[2], v[1], v[0])),
                "bottom",
            ),
            Face(Polygon((v[0], v[1], v[7], v[6])), "side0"),
            Face(Polygon((v[1], v[2], v[8], v[7])), "side1"),
            Face(Polygon((v[2], v[3], v[9], v[8])), "side2"),
            Face(Polygon((v[3], v[4], v[10], v[9])), "side3"),
            Face(Polygon((v[4], v[5], v[11], v[10])), "side4"),
            Face(Polygon((v[5], v[0], v[6], v[11])), "side5"),
        )