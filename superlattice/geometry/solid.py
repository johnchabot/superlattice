"""Abstract interfaces for solid geometry."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .point import Point3D
from .polygon import Polygon


class Solid(ABC):
    """Base interface for all 3D solids."""

    @property
    @abstractmethod
    def vertices(self) -> tuple[Point3D, ...]:
        ...

    @property
    @abstractmethod
    def faces(self) -> tuple[Polygon, ...]:
        ...
