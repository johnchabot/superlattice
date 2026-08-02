from math import radians, sin, cos
from pathlib import Path

from composition.canonical import (
    PRISM_RADIUS,
    SILOS,
)

from superlattice.camera.camera import Camera
from superlattice.geometry.hexagonal_prism import HexagonalPrism
from superlattice.geometry.point import Point3D
from superlattice.renderer.svg import render


# ------------------------------------------------------------------
# Canonical orbit camera
# ------------------------------------------------------------------

CAMERA_DISTANCE = 900.0
CAMERA_AZIMUTH = 0       # degrees (0 = straight-on)
CAMERA_HEIGHT = 100

TARGET = Point3D(
    0.0,
    0.0,
    200.0,
)

theta = radians(CAMERA_AZIMUTH)

eye = Point3D(
    CAMERA_DISTANCE * sin(theta),
    -CAMERA_DISTANCE * cos(theta),
    CAMERA_HEIGHT,
)

camera = Camera(
    eye=eye,
    target=TARGET,
    focal_length=600,
)

# ------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------

solids = [
    HexagonalPrism(
        center=spec.center,
        radius=PRISM_RADIUS,
        height=spec.height,
        rotation=spec.rotation,
    )
    for spec in SILOS
]

# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------

svg = render(
    solids,
    camera,
)

Path("generated").mkdir(exist_ok=True)

Path("generated/canonical_cluster.svg").write_text(svg)

print("Generated generated/canonical_cluster.svg")