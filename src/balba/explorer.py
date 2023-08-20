"""Methods related with file system management."""
from pathlib import Path

from balba.models import EXT_BOARD, EXT_PROJECT, EXT_SCHEMATIC, Project


def find_projects(path: str) -> list[Project]:
    """Return a list of all Kicad projects found under a certain directory.

    :param str path: Path where the search will start from
    :return: List of projects found
    """
    project_files = Path(path).glob(f"**/*{EXT_PROJECT}")

    return [
        Project(
            project=Path(project),
            board=Path(project).with_suffix(EXT_BOARD),
            schematic=Path(project).with_suffix(EXT_SCHEMATIC),
        )
        for project in project_files
    ]
