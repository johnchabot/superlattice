"""Canonical four-silo composition."""

from __future__ import annotations

from dataclasses import dataclass

from superlattice.geometry.point import Point3D

from composition.layout import ClusterLayout


PRISM_RADIUS = 100.0


@dataclass(frozen=True)
class SiloSpec:
    name: str
    center: Point3D
    height: float
    rotation: float


layout = ClusterLayout(
    radius=PRISM_RADIUS,
    overlap=100.0,
)

centers = layout.centers()

SILOS = [

    # Top (largest)
    SiloSpec(
        name="top",
        center=Point3D(0.0, -75.0, 0.0),
        height=400.0,
        rotation=90.0,
    ),

    # Right
    SiloSpec(
        name="right",
        center=Point3D(75.0, 0.0, 0.0),
        height=250.0,
        rotation=45.0,
    ),

    # Bottom
    SiloSpec(
        name="bottom",
        center=Point3D(0.0, 75.0, 0.0),
        height=260.0,
        rotation=0.0,
    ),

    # Left
    SiloSpec(
        name="left",
        center=Point3D(-75.0, 0.0, 0.0),
        height=290.0,
        rotation=135.0,
    ),
]