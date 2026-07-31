"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.point import Point3D
from superlattice.geometry.solid import Solid


CSS = """
<style>
svg {
    background: #ffffff;
}

polygon {
    fill: rgba(255,255,255,0.10);
    stroke: #404040;
    stroke-width: 1;
    vector-effect: non-scaling-stroke;
}

polygon.top {
    fill: rgba(255,255,255,0.18);
}

polygon.bottom {
    fill: rgba(255,255,255,0.03);
}

polygon.side0,
polygon.side1,
polygon.side2,
polygon.side3,
polygon.side4,
polygon.side5 {
    fill: rgba(255,255,255,0.08);
}
</style>
"""


def render(
    solids: Iterable[Solid],
    camera: Camera,
    width: int = 600,
    height: int = 600,
    debug: bool = False,
) -> str:

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="{-width//2} {-height//2} {width} {height}">',
        CSS,
    ]

    if debug:

        origin = camera.project(Point3D(0, 0, 0))
        x_axis = camera.project(Point3D(200, 0, 0))
        y_axis = camera.project(Point3D(0, 200, 0))
        z_axis = camera.project(Point3D(0, 0, 200))

        lines.append('<g id="debug-axes">')

        def draw_axis(a, b, colour):
            lines.append(
                f'<line '
                f'x1="{a.x:.2f}" y1="{-a.y:.2f}" '
                f'x2="{b.x:.2f}" y2="{-b.y:.2f}" '
                f'stroke="{colour}" stroke-width="2"/>'
            )

        draw_axis(origin, x_axis, "red")
        draw_axis(origin, y_axis, "green")
        draw_axis(origin, z_axis, "blue")

        lines.append(
            f'<circle '
            f'cx="{origin.x:.2f}" '
            f'cy="{-origin.y:.2f}" '
            f'r="4" '
            f'fill="black"/>'
        )

    for i, solid in enumerate(solids):

        lines.append(f'<g class="prism prism-{i}">')

        for face in solid.faces:

            pts = []

            for p in face.polygon.vertices:
                q = camera.project(p)
                pts.append(f"{q.x:.2f},{-q.y:.2f}")

            lines.append(
                f'<polygon '
                f'class="{face.name}" '
                f'points="{" ".join(pts)}"/>'
            )

        lines.append("</g>")

    if debug:
        lines.append("</g>")

    lines.append("</svg>")

    return "\n".join(lines)