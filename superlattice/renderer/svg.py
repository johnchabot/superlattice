"""SVG rendering utilities."""

from __future__ import annotations

from collections.abc import Iterable

from superlattice.camera.camera import Camera
from superlattice.geometry.point import Point3D
from superlattice.geometry.solid import Solid


CSS = """
<style>
:root {
    --scene-background: #090a0d;
    --grid-line: rgba(255,255,255,.045);
    --facet-top: rgba(255,255,255,.052);
    --facet-front: rgba(255,245,248,.034);
    --facet-left: rgba(240,255,250,.034);
    --facet-right: rgba(240,246,255,.034);
    --facet-rear: rgba(255,250,240,.034);
    --edge-energy: rgba(255,255,255,.28);
    --edge-width: .9;
    --rim-energy: rgba(255,255,255,.18);
    --rim-width: .65;
}

svg {
    background: var(--scene-background);
}

.scene-grid line {
    stroke: var(--grid-line);
    stroke-width: 1;
}

.face {
    vector-effect: non-scaling-stroke;
    stroke-linejoin: round;
    stroke-linecap: round;
}

.render-fill {
    stroke: none;
}

.face-top.surface-density {

    fill: white;

    opacity: .020;

    stroke: none;

}

.face-side.surface-density {

    fill: url(#glass-face);

    opacity: .085;

    stroke: none;

}

.face-bottom.surface-density {

    opacity: 0;

}

.render-fill.face-top,
.render-fill.face-side,
.render-fill.face-bottom {

    fill: url(#glass-face);

    opacity: .28;

}




.render-rim {
    fill: none;
    stroke: var(--rim-energy);
    stroke-width: var(--rim-width);
    stroke-linejoin: round;
    stroke-linecap: round;
    vector-effect: non-scaling-stroke;
}

.render-edge {
    fill: none;
    stroke: var(--edge-energy);
    stroke-width: var(--edge-width);
    stroke-linejoin: round;
    stroke-linecap: round;
    vector-effect: non-scaling-stroke;
}

.optical-highlight {

    fill: white;

    opacity: .045;

    stroke: none;

}

.edge-major { stroke-width: 1.1; }
.edge-normal { stroke-width: .9; }
.edge-minor { stroke-width: .6; opacity: .55; }
</style>
"""


def face_classes(face_name: str) -> str:
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
        classes.append(f"face-side-{face_name[-1]}")

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

    <linearGradient id="facetGlass" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity=".20"/>
        <stop offset="45%" stop-color="#6ecbff" stop-opacity=".10"/>
        <stop offset="100%" stop-color="#ff7de7" stop-opacity=".16"/>
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

    roles = [
        "member-front",
        "member-left",
        "member-right",
        "member-rear",
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
            projected_faces.append((face, pts))
        for face, pts in projected_faces:

            classes = face_classes(face.name)

            fill = ""
            if face.name == "top":
                fill = ' style="fill:url(#glass-face); opacity:.34;"'
            elif face.name == "bottom":
                fill = ' style="fill:url(#glass-face); opacity:.10;"'
            elif face.name.startswith("side"):
                side = face.name[-1]
                if side in ("0", "2", "4"):
                    fill = ' style="fill:url(#glass-face); opacity:.24;"'
                else:
                    fill = ' style="fill:url(#glass-face); opacity:.16;"'

            lines.append(
                f'<polygon class="{classes}"{fill} points="{" ".join(pts)}"/>'
            )

            if face.name != "bottom":
                lines.append(
                    f'<polygon '
                    f'class="{classes} surface-density" '
                    f'points="{" ".join(pts)}"/>'
                )

            lines.append(
                f'<polygon class="{classes} optical-highlight" points="{" ".join(pts)}"/>'
            )

            rim_classes = classes.replace("render-fill", "render-rim")
            lines.append(
                f'<polygon class="{rim_classes}" points="{" ".join(pts)}"/>'
            )


            edge_classes = classes.replace("render-fill", "render-edge")
            if face.name == "top":
                edge_classes += " edge-major"
            elif face.name == "bottom":
                edge_classes += " edge-minor"
            else:
                edge_classes += " edge-normal"

            lines.append(
                f'<polygon class="{edge_classes}" points="{" ".join(pts)}"/>'
            )

        lines.append("</g>")

    lines.append("</g>")
    lines.append("</g>")
    lines.append("</svg>")

    return "\n".join(lines)