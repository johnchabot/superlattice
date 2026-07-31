"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.point import Point3D
from superlattice.geometry.solid import Solid


CSS = """
<style>

:root {

    --scene-background: rgb(255 255 255);

    --edge-energy: rgba(245,248,252,.32);
    --edge-colour: rgb(64 64 64);
    --edge-width: 1;
    --edge-opacity: 1.0;

    --transmission-top: rgba(255,255,255,0.045);
    --transmission-side: rgba(255,255,255,0.022);
    --material-bottom: rgba(255,255,255,0.010);



}

/* ------------------------------------------------------------------ */
/* Scene */
/* ------------------------------------------------------------------ */

svg {
    background: var(--scene-background);
}

/* ------------------------------------------------------------------ */
/* Geometry */
/* ------------------------------------------------------------------ */

.face {

    stroke: rgba(245,248,252,.32);

    stroke-width: .85;
    stroke: var(--edge-energy);
    vector-effect: non-scaling-stroke;

    stroke-linejoin: round;
    stroke-linecap: round;

}

.face:hover {

    stroke: rgba(255,255,255,.9);

}

/* ------------------------------------------------------------------ */
/* Material */
/* ------------------------------------------------------------------ */

.face-top {

    fill: var(--material-top);

}

.face-side {

    fill: rgba(255,255,255,.028);

}

.face-top {

    fill: rgba(255,255,255,.040);

}

.face-bottom {

    fill: rgba(255,255,255,.012);

}

/* ------------------------------------------------------------------ */
/* Future placeholders */
/* ------------------------------------------------------------------ */

.scene {}
.neighbourhood {}

.member {}

.render {}
.render-fill {}
.render-edge {}

.material {}
.material-transmission {}
.material-density {}

.optical {}
.optical-base {}
.optical-density {}
.optical-highlight {}

/* ------------------------------------------------------------------ */
/* Member */
/* ------------------------------------------------------------------ */

.member-front {

}

.member-left {

}

.member-right {

}

.member-rear {

}

</style>
"""


def face_classes(face_name: str) -> str:
    """Return semantic CSS classes for a face."""

    classes = [
        "render",
        "render-fill",
        "face",
        "material",
        "material-transmission",
        "optical",
        "optical-base",
    ]

    if face_name == "top":

        classes.append("face-top")

    elif face_name == "bottom":

        classes.append("face-bottom")

    else:

        classes.append("face-side")

    return " ".join(classes)


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
        '<g class="scene">',
        '<g class="neighbourhood">',
    ]

    if debug:

        origin = camera.project(Point3D(0, 0, 0))
        x_axis = camera.project(Point3D(200, 0, 0))
        y_axis = camera.project(Point3D(0, 200, 0))
        z_axis = camera.project(Point3D(0, 0, 200))

        lines.append('<g class="debug">')

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

        lines.append("</g>")

    roles = [
        "member-front",
        "member-left",
        "member-right",
        "member-rear",
    ]

    for i, solid in enumerate(solids):

        role = roles[i] if i < len(roles) else "member"

        lines.append(
        f'<g class="member {role}">'
        )

        for face in solid.faces:

            pts = []

            for p in face.polygon.vertices:
                q = camera.project(p)
                pts.append(f"{q.x:.2f},{-q.y:.2f}")

            lines.append(
                f'<polygon '
                f'class="{face_classes(face.name)}" '
                f'points="{" ".join(pts)}"/>'
            )

        lines.append("</g>")

    lines.append("</g>")
    lines.append("</g>")
    lines.append("</svg>")

    return "\n".join(lines)