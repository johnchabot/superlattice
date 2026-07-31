"""Abstract interfaces for solid geometry."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .edge import Edge
from .face import Face
from .point import Point3D


class Solid(ABC):
    """Base interface for all 3D solids."""

    @property
    @abstractmethod
    def vertices(self) -> tuple[Point3D, ...]:
        """All vertices of the solid."""
        ...

    @property
    @abstractmethod
    def edges(self) -> tuple[Edge, ...]:
        """All edges of the solid."""
        ...

    @property
    @abstractmethod
    def faces(self) -> tuple[Face, ...]:
        """All faces of the solid."""
        ...