"""Canonical four-silo composition."""

from __future__ import annotations

from dataclasses import dataclass

from superlattice.geometry.point import Point3D


PRISM_RADIUS = 100.0


@dataclass(frozen=True)
class SiloSpec:
    name: str
    center: Point3D
    height: float
    rotation: float


SILOS = [

    # Top (largest)
    SiloSpec(
        name="top",
        center=Point3D(0.0, -75.0, 0.0),
        height=360.0,
        rotation=90.0,
    ),

    # Right
    SiloSpec(
        name="right",
        center=Point3D(75.0, 0.0, 0.0),
        height=260.0,
        rotation=45.0,
    ),

    # Bottom
    SiloSpec(
        name="bottom",
        center=Point3D(0.0, 75.0, 0.0),
        height=220.0,
        rotation=0.0,
    ),

    # Left
    SiloSpec(
        name="left",
        center=Point3D(-75.0, 0.0, 0.0),
        height=300.0,
        rotation=135.0,
    ),
]