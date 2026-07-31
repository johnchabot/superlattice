from pathlib import Path

from composition.canonical import (
    PRISM_RADIUS,
    PRISM_ROTATION,
    SILOS,
)

from superlattice.camera.camera import Camera
from superlattice.geometry.hexagonal_prism import HexagonalPrism
from superlattice.renderer.svg import render


camera = Camera()

solids = [
    HexagonalPrism(
        center=spec.center,
        radius=PRISM_RADIUS,
        height=spec.height,
        rotation=PRISM_ROTATION,
    )
    for spec in SILOS
]

svg = render(
    solids,
    camera,
    debug=True,
)

Path("generated").mkdir(exist_ok=True)

Path("generated/canonical_cluster.svg").write_text(svg)

print("Generated generated/canonical_cluster.svg")