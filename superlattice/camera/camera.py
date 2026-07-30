"""Simple perspective camera."""

from __future__ import annotations

from dataclasses import dataclass

from superlattice.geometry.point import Point3D


@dataclass(frozen=True)
class Point2D:
    x: float
    y: float


@dataclass(frozen=True)
class Camera:
    focal_length: float = 500.0

    def project(self, point: Point3D) -> Point2D:
        z = point.z + self.focal_length
        return Point2D(
            x=self.focal_length * point.x / z,
            y=self.focal_length * point.y / z,
        )
