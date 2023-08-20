"""Collection of classes that represent Kicad entities."""
from dataclasses import dataclass
from pathlib import Path

EXT_BOARD = ".kicad_pcb"
EXT_PROJECT = ".kicad_pro"
EXT_SCHEMATIC = ".kicad_sch"


@dataclass
class Project:
    """Main files that form part of a Kicad project."""

    board: Path
    project: Path
    schematic: Path


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
