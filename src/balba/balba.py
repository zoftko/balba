"""Implementation of the program's workflow"""
from pathlib import Path

from click import echo, style
from yaml import CLoader, load

from balba.builder import Builder
from balba.driver import Driver
from balba.explorer import find_project_files, read_frontmatter
from balba.models import Project


def balba_run(src: str, output: str) -> int:
    """Perform the website building process."""
    version = Driver.version()
    if not version:
        echo(style("Could not find a valid kicad-cli version", fg="red"))
        return 127

    config_file = Path(src) / "balba.yaml"
    if not config_file.exists():
        echo(style("Could not find a configuration file", fg="red"))
        return 126

    config = load(config_file.read_bytes(), CLoader)
    builder = Builder(Path(output), config)

    echo(f"Using kicad-cli {version}")
    echo(f"Looking for projects in {src}")

    projects: list[Project] = []
    project_files = find_project_files(src)
    for files in project_files:
        with files.readme.open("r", encoding="utf-8") as readme_fd:
            front_matter = read_frontmatter(readme_fd)

        projects.append(Project(**front_matter, files=files))

    builder.build_index(projects)

    echo(f"Generating website in {output}")

    return 0
