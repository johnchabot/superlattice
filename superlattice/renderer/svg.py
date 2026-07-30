"""SVG rendering utilities."""

from __future__ import annotations

from superlattice.camera.camera import Camera
from superlattice.geometry.polygon import Polygon


def render(polygons: list[Polygon], camera: Camera, width:int=600, height:int=600)->str:
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{-width//2} {-height//2} {width} {height}">']
    for poly in polygons:
        pts=[]
        for p in poly.vertices:
            q=camera.project(p)
            pts.append(f'{q.x:.2f},{-q.y:.2f}')
        lines.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="black"/>')
    lines.append('</svg>')
    return '\n'.join(lines)
