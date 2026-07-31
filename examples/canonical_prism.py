from pathlib import Path

from superlattice.camera.camera import Camera
from superlattice.geometry.hexagonal_prism import HexagonalPrism
from superlattice.geometry.point import Point3D
from superlattice.renderer.svg import render

prism = HexagonalPrism(
    center=Point3D(0, 0, 0),
    radius=100,
    height=200,
)

camera = Camera()

svg = render(prism, camera)

Path("generated").mkdir(exist_ok=True)

Path("generated/canonical_prism.svg").write_text(svg)

print("Generated generated/canonical_prism.svg")