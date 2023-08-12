"""Collection of classes that represent Kicad entities."""
from dataclasses import dataclass


@dataclass
class Layer:
    """Kicad Layer as shown on the stackup section."""

    name: str
    type: str
    thickness: float


@dataclass
class Board:
    """A pcbnew board."""

    layers: list[Layer]
