from dataclasses import dataclass

from superlattice.geometry.point import Point3D


@dataclass(frozen=True)
class ClusterLayout:

    radius: float
    overlap: float

    def centers(self):

        touch = self.radius * 1.7320508075688772   # √3 × radius

        spacing = touch - self.overlap

        top = Point3D(
            0.0,
            -spacing * 0.55,
            0.0,
        )

        right = Point3D(
            spacing * 0.50,
            -spacing * 0.12,
            0.0,
        )

        bottom = Point3D(
            0.0,
            spacing * 0.32,
            0.0,
        )

        left = Point3D(
            -spacing * 0.50,
            -spacing * 0.12,
            0.0,
        )

        print("Top   :", top)
        print("Right :", right)
        print("Bottom:", bottom)
        print("Left  :", left)

        return [
            top,
            right,
            bottom,
            left,
        ]


        return [
            top,
            right,
            bottom,
            left,
        ]