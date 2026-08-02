"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.point import Point3D
from superlattice.geometry.solid import Solid


CSS = """
<style>
:root{

  --scene-background: rgb(236 239 244);

  /* Transmission */
  --transmission-top: rgba(255,255,255,.010);
  --transmission-bottom: rgba(255,255,255,.002);
  --transmission-front: rgba(255,248,248,.005);
  --transmission-left: rgba(248,255,250,.005);
  --transmission-right: rgba(248,251,255,.005);
  --transmission-rear: rgba(255,252,248,.005);

  --material-core: var(--transmission-bottom);

  /* Edges */
  --edge-energy: rgba(80,85,92,.28);
  --edge-width: 1.15;

  /* Rim */
  --rim-energy: rgba(255,255,255,.55);
  --rim-width: .65;
}

svg{
  background:var(--scene-background);
}

.face{
  vector-effect:non-scaling-stroke;
  stroke-linejoin:round;
  stroke-linecap:round;
}

.face:hover{
  stroke:rgba(255,255,255,.9);
}


.material-core.orientation-bottom {
    fill: var(--material-core);
}

/* Material aliases */
.material-shell {
    opacity: .22;
}

.material-shell.orientation-top,
.material-shell.orientation-side {
    fill: url(#facetGlass);
}


.render-edge{
  fill:none;
  stroke:var(--edge-energy);
  stroke-width:var(--edge-width);
  stroke-linejoin:round;
  stroke-linecap:round;
  vector-effect:non-scaling-stroke;
}

.render-rim{
  fill:none;
  stroke:var(--rim-energy);
  stroke-width:var(--rim-width);
  stroke-linejoin:round;
  stroke-linecap:round;
  vector-effect:non-scaling-stroke;
  opacity:.35;
}

.edge-glow{
    fill:none;
    stroke:white;
    stroke-width:.35;
    opacity:.35;
    vector-effect:non-scaling-stroke;
    stroke-linejoin:round;
    stroke-linecap:round;
}

.optical-highlight{
  fill:none;
 stroke: rgba(255,255,255,.18);
  stroke-width:.18;
  stroke-linejoin:round;
  stroke-linecap:round;
  vector-effect:non-scaling-stroke;
  mix-blend-mode:screen;
}

.material-shell.orientation-side {
    fill: url(#facetGlass);
}

.surface-density {
    fill: url(#densityGlass);
    mix-blend-mode: multiply;
    opacity: .30;
}

.edge-major{stroke-width:1.10;}
.edge-normal{stroke-width:.85;}
.edge-minor{
  stroke-width:.55;
  opacity:.55;
}
</style>
"""


def face_classes(face_name: str) -> str:
    """Return semantic CSS classes for a face."""
    print(face_name)
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

        classes.extend([
            "face-top",
            "material-shell",
            "orientation-top",
        ])

    elif face_name == "bottom":

        classes.extend([
            "face-bottom",
            "material-core",
            "orientation-bottom",
        ])


    elif face_name.startswith("side"):

        classes.extend([
            "face-side",
            "material-shell",
            "orientation-side",
        ])

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
    <filter id="gemShadow" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="14" result="blur"/>
        <feOffset in="blur" dx="0" dy="10" result="offset"/>
        <feFlood flood-color="#000" flood-opacity="0.45" result="flood"/>
        <feComposite in="flood" in2="offset" operator="in" result="shadow"/>
        <feMerge>
            <feMergeNode in="shadow"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <linearGradient id="densityGlass"
                    x1="0%"
                    y1="0%"
                    x2="0%"
                    y2="100%">
        <stop offset="0%"   stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="45%"  stop-color="#d9e2ec" stop-opacity=".08"/>
        <stop offset="100%" stop-color="#7a8798" stop-opacity=".28"/>
    </linearGradient>


    <linearGradient id="facetGlass"
                    x1="0%"
                    y1="0%"
                    x2="100%"
                    y2="100%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="100%" stop-color="#d8e6f4"/>
    </linearGradient>

    <linearGradient id="edgeFade" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity=".05"/>
        <stop offset="50%" stop-color="#ffffff" stop-opacity=".50"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity=".05"/>
    </linearGradient>

    <linearGradient id="glass-face"
                    x1="0%"
                    y1="0%"
                    x2="100%"
                    y2="100%">

        <stop offset="0%" stop-color="#ffffff" stop-opacity=".18"/>
        <stop offset="35%" stop-color="#8fdcff" stop-opacity=".08"/>
        <stop offset="70%" stop-color="#bfa8ff" stop-opacity=".06"/>
        <stop offset="100%" stop-color="#ff84df" stop-opacity=".14"/>

    </linearGradient>

</defs>
""",
        '<g class="scene">',
        '<g class="scene-grid">',
    ]

    grid_step = 60
    half_w = width // 2
    half_h = height // 2

    for x in range(-half_w, half_w + 1, grid_step):
        lines.append(f'<line x1="{x}" y1="{-half_h}" x2="{x}" y2="{half_h}"/>')
    for y in range(-half_h, half_h + 1, grid_step):
        lines.append(f'<line x1="{-half_w}" y1="{y}" x2="{half_w}" y2="{y}"/>')

    lines += [
        "</g>",
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
                f'<line x1="{a.x:.2f}" y1="{-a.y:.2f}" '
                f'x2="{b.x:.2f}" y2="{-b.y:.2f}" '
                f'stroke="{colour}" stroke-width="2"/>'
            )

        draw_axis(origin, x_axis, "red")
        draw_axis(origin, y_axis, "green")
        draw_axis(origin, z_axis, "blue")
        lines.append(
            f'<circle cx="{origin.x:.2f}" cy="{-origin.y:.2f}" r="4" fill="black"/>'
        )
        lines.append("</g>")

    render_faces = []
    
    roles = [
        "member-front",
        "member-front",
        "member-front",
        "member-front",
    ]

    for i, solid in enumerate(solids):
        role = roles[i] if i < len(roles) else "member"

        lines.append(
            f'<g class="member {role}" style="filter:url(#gemShadow);">'
        )

        projected_faces = []
        for face in solid.faces:
            
            pts = []
            for p in face.polygon.vertices:
                q = camera.project(p)
                pts.append(f"{q.x:.2f},{-q.y:.2f}")
            depth = sum(v.z for v in face.polygon.vertices) / len(face.polygon.vertices)

            projected_faces.append(
                (
                    depth,
                    role,
                    face,
                    pts,
                )
            )
        render_faces.extend(projected_faces)


        for depth, role, face, pts in projected_faces:

            classes = face_classes(face.name)


 
            if True:
                lines.append(
                    f'<polygon '
                    f'class="{classes}" '
                    f'points="{" ".join(pts)}"/>'
                )

                lines.append(
                    f'<polygon '
                    f'class="{classes} surface-density" '
                    f'points="{" ".join(pts)}"/>'
                )

            lines.append(
                f'<polygon class="face optical-highlight material-shell-pass" '
                f'points="{" ".join(pts)}"/>'
            )

            if face.name == "top":
                orientation = "orientation-top"
            elif face.name == "bottom":
                orientation = "orientation-bottom"
            else:
                orientation = "orientation-side"

            rim_classes = f"face render-rim material-boundary {orientation}"

            lines.append(
                f'<polygon class="{rim_classes}" points="{" ".join(pts)}"/>'
            )

            edge_classes = f"face render-edge material-boundary {orientation}"

            if face.name == "top":
                edge_classes += " edge-major"
            elif face.name == "bottom":
                edge_classes += " edge-minor"
            else:
                edge_classes += " edge-normal"

            lines.append(
                f'<polygon class="{edge_classes}" points="{" ".join(pts)}"/>'
            )

            lines.append(
                f'<polygon class="face edge-glow" points="{" ".join(pts)}"/>'
            )


        lines.append("</g>")

    lines.append("</g>")
    lines.append("</g>")
    lines.append("</svg>")

    return "\n".join(lines)