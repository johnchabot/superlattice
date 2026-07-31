from superlattice.geometry.hexagonal_prism import HexagonalPrism
from superlattice.geometry.point import Point3D

p = HexagonalPrism(
    center=Point3D(0, 0, 0),
    radius=100,
    height=200,
    rotation=30,
)

print(p.vertices)