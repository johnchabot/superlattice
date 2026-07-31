from dataclasses import dataclass

from superlattice.geometry.point import Point3D


# Geometry (rarely changes)

PRISM_RADIUS = 100.0
PRISM_ROTATION = 45.0      # Adjust if your vertex ordering requires a different value


@dataclass(frozen=True)
class SiloSpec:
    name: str
    center: Point3D
    height: float


# Composition (we'll iterate on this)

SILOS = (
    SiloSpec(
        "rear",
        Point3D(0, -80, 0),
        420,
    ),
    SiloSpec(
        "left",
        Point3D(-70, -10, 0),
        340,
    ),
    SiloSpec(
        "right",
        Point3D(70, -10, 0),
        300,
    ),
    SiloSpec(
        "front",
        Point3D(0, 70, 0),
        240,
    ),
)