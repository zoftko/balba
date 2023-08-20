# pylint: disable=missing-module-docstring,missing-function-docstring

from pathlib import Path

from balba.explorer import EXT_BOARD, EXT_PROJECT, EXT_SCHEMATIC, find_projects


def test_find_projects(tmpdir):
    test_projects = ["blinker", "buck", "boost"]
    for project in test_projects:
        folder = Path(tmpdir) / project
        folder.mkdir()

        (folder / f"{folder.name}{EXT_BOARD}").touch()
        (folder / f"{folder.name}{EXT_PROJECT}").touch()
        (folder / f"{folder.name}{EXT_SCHEMATIC}").touch()

    found_projects = find_projects(tmpdir)
    assert len(found_projects) == 3
    for project in found_projects:
        project_name = project.project.parent.name

        assert Path(tmpdir / project_name / f"{project_name}{EXT_BOARD}") == project.board
        assert Path(tmpdir / project_name / f"{project_name}{EXT_PROJECT}") == project.project
        assert Path(tmpdir / project_name / f"{project_name}{EXT_SCHEMATIC}") == project.schematic
