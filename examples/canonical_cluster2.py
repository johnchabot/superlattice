from pathlib import Path

from superlattice.camera.camera import Camera
from superlattice.geometry.hexagonal_prism import HexagonalPrism
from superlattice.geometry.point import Point3D
from superlattice.renderer.svg import render

camera = Camera()

solids = [
    HexagonalPrism(
        center=Point3D(0, -80, 0),
        radius=100,
        height=420,
    ),
    HexagonalPrism(
        center=Point3D(-80, 40, 0),
        radius=100,
        height=340,
    ),
    HexagonalPrism(
        center=Point3D(80, 40, 0),
        radius=100,
        height=300,
    ),
    HexagonalPrism(
        center=Point3D(0, 120, 0),
        radius=100,
        height=240,
    ),
]

svg = render(solids, camera)

Path("generated").mkdir(exist_ok=True)
Path("generated/canonical_cluster.svg").write_text(svg)

print("Generated generated/canonical_cluster.svg")