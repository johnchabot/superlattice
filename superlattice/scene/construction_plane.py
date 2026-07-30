"""Canonical construction plane.

Every geometric object in a Superlattice scene is ultimately anchored to a construction plane.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConstructionPlane:
    """Canonical isosceles trapezoid construction plane."""

    front_width: float = 400.0
    back_width: float = 200.0
    depth: float = 250.0

    @property
    def is_valid(self) -> bool:
        return (
            self.front_width > self.back_width > 0
            and self.depth > 0
        )
