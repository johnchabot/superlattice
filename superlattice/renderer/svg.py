"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.point import Point3D
from superlattice.geometry.solid import Solid


CSS = """
<style>

/*
CRYSTAL MANIFEST

1.
Nothing is opaque.

2.
Nothing calls attention to itself.

3.
Edges describe thickness.

4.
Colour emerges through accumulation.

5.
Every layer contributes.

6.
No single layer defines the object.
*/


:root {


--scene-background: rgb(236 239 244);

    /* Transmission */

.render-fill.face-top {

    fill: rgba(255,255,255,.010);

}

.member-front .render-fill.face-side {

    fill: rgba(255,248,248,.005);

}

.member-left .render-fill.face-side {

    fill: rgba(248,255,250,.005);

}

.member-right .render-fill.face-side {

    fill: rgba(248,251,255,.005);

}

.member-rear .render-fill.face-side {

    fill: rgba(255,252,248,.005);

}

.render-fill.face-bottom {

    fill: rgba(255,255,255,.002);

}

    /* Edge */

    --edge-energy: rgb(128,132,140);
    --edge-width: .85;

    /* Rim */

    --rim-energy: rgba(255,255,255,.18);
    --rim-width: .65;

    --member-bias: 1.0;

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

    vector-effect: non-scaling-stroke;

    stroke-linejoin: round;
    stroke-linecap: round;

}


.geometry {

}

.transmission {

}


.render-edge {

    fill: none;

    stroke: var(--edge-energy);

    stroke-width: var(--edge-width);

    stroke-linejoin: round;
    stroke-linecap: round;

    vector-effect: non-scaling-stroke;

}


.face:hover {

    stroke: rgba(255,255,255,.9);

}

/* ------------------------------------------------------------------ */
/* Material */
/* ------------------------------------------------------------------ */



/* ------------------------------------------------------------------ */
/* Future placeholders */
/* ------------------------------------------------------------------ */

.scene {}
.neighbourhood {}

.member {}

.render {}
.render-fill {}

.render-fill.face-top {

    fill: var(--transmission-top);

}



.render-fill.face-bottom {

    fill: var(--transmission-bottom);

}

.render-edge {

    fill: none;

    stroke: rgba(115,120,130,.42);

    stroke-width: 1.15;

    stroke-linejoin: round;
    stroke-linecap: round;

    vector-effect: non-scaling-stroke;

}

.render-rim {

    fill: none;

    stroke: rgba(255,255,255,.55);

    stroke-width: var(--rim-width);

    stroke-linejoin: round;
    stroke-linecap: round;

    vector-effect: non-scaling-stroke;

    opacity: .85;

}

.material {}
.material-transmission {}
.material-density {}

.optical {}
.optical-base {}
.optical-density {}
.optical-highlight {

    fill: none;

    stroke: rgba(255,255,255,.28);

    stroke-width: .18;

    stroke-linejoin: round;
    stroke-linecap: round;

    vector-effect: non-scaling-stroke;

    mix-blend-mode: screen;

}

/* ------------------------------------------------------------------ */
/* Member */
/* ------------------------------------------------------------------ */

.member-front {

    --transmission-scale: 1.00;

}

.member-left {

    --transmission-scale: 0.98;

}

.member-right {

    --transmission-scale: 1.02;

}

.member-rear {

    --transmission-scale: 1.05;

}


.edge-major {

    stroke-width: 1.10;

}

.edge-normal {

    stroke-width: .85;

}

.edge-minor {

    stroke-width: .55;

    opacity: .55;

}


</style>
"""


def face_classes(face_name: str) -> str:
    """Return semantic CSS classes for a face."""

    classes = [
        "render",
        "render-fill",

        "geometry",
        "face",

        "transmission",
        "material",
        "material-transmission",

        "optical",
        "optical-base",
    ]

    if face_name == "top":

        classes.append("face-top")

    elif face_name == "bottom":

        classes.append("face-bottom")

    elif face_name.startswith("side"):

        classes.append("face-side")

        side = face_name[-1]

        classes.append(f"face-side-{side}")

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

    """
<defs>

    <linearGradient id="edge-rim"
                    x1="0%"
                    y1="0%"
                    x2="100%"
                    y2="0%">

        <stop offset="0%" stop-color="white" stop-opacity="0.00"/>

        <stop offset="30%" stop-color="white" stop-opacity="0.18"/>

        <stop offset="70%" stop-color="white" stop-opacity="0.18"/>

        <stop offset="100%" stop-color="white" stop-opacity="0.00"/>

    </linearGradient>



</defs>
""",

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
            f'<g class="member {role}" '
            f'style="--member-transmission:1.0;">'
        )

        fill_pass = []
        highlight_pass = []
        rim_pass = []
        edge_pass = []
        projected_faces = []

        for face in solid.faces:

            pts = []

            for p in face.polygon.vertices:
                q = camera.project(p)
                pts.append(f"{q.x:.2f},{-q.y:.2f}")

            projected_faces.append((face, pts))

        for face, pts in projected_faces:

            classes = face_classes(face.name)

            for face, pts in projected_faces:

                classes = face_classes(face.name)

                fill = ""

                if face.name.startswith("side"):

                    fill = (
                        ' style="fill:url(#glass-face);"'
                    )

                lines.append(
                    f'<polygon '
                    f'class="{classes}"'
                    f'{fill} '
                    f'points="{" ".join(pts)}"/>'
                )

            #
            # Specular highlight
            #

            lines.append(
                f'<polygon '
                f'class="{classes} optical-highlight" '
                f'points="{" ".join(pts)}"/>'
            )

            #
            # Pass 2 — Rim
            #

            rim_classes = classes.replace(
                "render-fill",
                "render-rim",
            )

            lines.append(
                f'<polygon '
                f'class="{rim_classes}" '
                f'points="{" ".join(pts)}"/>'
            )

            #
            # Pass 3 — Edge
            #

            edge_classes = classes.replace(
                "render-fill",
                "render-edge",
            )

            if face.name == "top":
                edge_classes += " edge-major"

            elif face.name == "bottom":
                edge_classes += " edge-minor"

            else:
                edge_classes += " edge-normal"

            lines.append(
                f'<polygon '
                f'class="{edge_classes}" '
                f'points="{" ".join(pts)}"/>'
            )

        lines.append("</g>")

    lines.append("</g>")
    lines.append("</g>")
    lines.append("</svg>")

    return "\n".join(lines)