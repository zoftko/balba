"""Implementation of the program's workflow"""
from pathlib import Path

from click import echo, style
from markdown import markdown
from yaml import CLoader, load

from balba.builder import Builder
from balba.driver import Driver
from balba.explorer import find_project_files, read_frontmatter
from balba.models import Project


def balba_run(src: str, output: str, dev: bool) -> int:
    """Perform the website building process."""
    driver = Driver()
    version = driver.version()
    if not version:
        echo(style("Could not find a valid kicad-cli version", fg="red"))
        return 127

    src_path = Path(src).absolute()
    config_file = src_path / "balba.yaml"
    if not config_file.exists():
        echo(style("Could not find a configuration file", fg="red"))
        return 126

    output_path = Path(output).absolute()
    builder = Builder(
        output_path,
        driver,
        load(config_file.read_bytes(), CLoader),
        dev,
    )

    echo(f"Using kicad-cli {version}")
    echo(f"Looking for projects in {src}")

    projects: list[Project] = []
    for files in find_project_files(src):
        with files.readme.open("r", encoding="utf-8") as readme_fd:
            front_matter = read_frontmatter(readme_fd)
            content = markdown(readme_fd.read())

        projects.append(Project(**front_matter, content=content, files=files))

    echo(f"Generating website in {output_path}")
    builder.build_website(projects)

    return 0
