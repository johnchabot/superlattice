from superlattice.geometry.point import Point3D
from superlattice.geometry.regular_hexagon import RegularHexagon

print("Rotation 0°")
for p in RegularHexagon(
    center=Point3D(0, 0, 0),
    radius=100,
    rotation=0,
).polygon().vertices:
    print(p)

print()

print("Rotation 30°")
for p in RegularHexagon(
    center=Point3D(0, 0, 0),
    radius=100,
    rotation=30,
).polygon().vertices:
    print(p)