"""Perspective look-at camera."""

from __future__ import annotations

from dataclasses import dataclass
import math

from superlattice.geometry.point import Point3D


@dataclass(frozen=True)
class Point2D:
    x: float
    y: float


@dataclass(frozen=True)
class CameraPoint:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Camera:

    # Camera position
    eye: Point3D = Point3D(-500.0, -700.0, 350.0)

    # Where the camera is looking
    target: Point3D = Point3D(0.0, 0.0, 180.0)

    focal_length: float = 600.0

    # ------------------------------------------------------------------
    # Camera basis
    # ------------------------------------------------------------------

    def _basis(self):

        # Forward

        fx = self.target.x - self.eye.x
        fy = self.target.y - self.eye.y
        fz = self.target.z - self.eye.z

        fl = math.sqrt(fx * fx + fy * fy + fz * fz)

        fx /= fl
        fy /= fl
        fz /= fl

        # World up

        ux = 0.0
        uy = 0.0
        uz = 1.0

        # Right = Forward × Up

        rx = fy * uz - fz * uy
        ry = fz * ux - fx * uz
        rz = fx * uy - fy * ux

        rl = math.sqrt(rx * rx + ry * ry + rz * rz)

        rx /= rl
        ry /= rl
        rz /= rl

        # Corrected Up = Right × Forward

        ux = ry * fz - rz * fy
        uy = rz * fx - rx * fz
        uz = rx * fy - ry * fx

        return (
            (rx, ry, rz),
            (ux, uy, uz),
            (fx, fy, fz),
        )

    # ------------------------------------------------------------------
    # World -> Camera
    # ------------------------------------------------------------------

    def world_to_camera(
        self,
        point: Point3D,
    ) -> CameraPoint:

        right, up, forward = self._basis()

        px = point.x - self.eye.x
        py = point.y - self.eye.y
        pz = point.z - self.eye.z

        cx = (
            px * right[0]
            + py * right[1]
            + pz * right[2]
        )

        cy = (
            px * up[0]
            + py * up[1]
            + pz * up[2]
        )

        cz = (
            px * forward[0]
            + py * forward[1]
            + pz * forward[2]
        )

        return CameraPoint(
            x=cx,
            y=cy,
            z=cz,
        )

    # ------------------------------------------------------------------
    # Camera -> Screen
    # ------------------------------------------------------------------

    def project_camera(
        self,
        point: CameraPoint,
    ) -> Point2D:

        z = max(point.z, 0.001)

        return Point2D(
            x=self.focal_length * point.x / z,
            y=self.focal_length * point.y / z,
        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def project(
        self,
        point: Point3D,
    ) -> Point2D:

        return self.project_camera(
            self.world_to_camera(point)
        )