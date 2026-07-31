"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.solid import Solid


def render(
    solids: Iterable[Solid],
    camera: Camera,
    width: int = 600,
    height: int = 600,
) -> str:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="{-width//2} {-height//2} {width} {height}">'
    ]

    for solid in solids:
        for face in solid.faces:
            pts = []

            for p in face.polygon.vertices:
                q = camera.project(p)
                pts.append(f"{q.x:.2f},{-q.y:.2f}")

            lines.append(
                f'<polygon points="{" ".join(pts)}" '
                f'fill="none" stroke="black"/>'
            )

    lines.append("</svg>")

    return "\n".join(lines)