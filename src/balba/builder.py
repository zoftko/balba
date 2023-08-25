"""All website building is performed in this file."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

from jinja2 import Environment, PackageLoader, select_autoescape

from balba.driver import Driver
from balba.models import Project


class Builder:
    """Object in charge of building the website components."""

    def __init__(self, output_directory: Path, driver: Driver, config: dict, dev: bool):
        self.config = config
        self.driver = driver
        self.output_directory = output_directory
        self.environment = Environment(loader=PackageLoader("balba"), autoescape=select_autoescape())

        self.environment.globals.update(config)
        self.environment.globals["year"] = datetime.today().year
        self.environment.globals["build_url"] = self.build_url

        self.output_directory.mkdir(exist_ok=True)
        (self.output_directory / "boards").mkdir(exist_ok=True)
        (self.output_directory / "balba.css").write_text(
            self.environment.get_template("balba.css").render(), encoding="utf-8"
        )

        if dev:
            self.environment.globals["base_url"] = "/"

    def build_url(self, path: str | list[str]):
        """Build a complete URL based on the website's base URL"""
        if isinstance(path, str):
            path = [path]

        return urljoin(self.environment.globals["base_url"], "/".join(path))

    def board_image_path(self, project: Project) -> Path:
        """
        Obtain a project's board image path.
        :param project: Project to obtain the path for
        :return: Path to the project's board image, it may not exist yet.
        """
        return Path(self.output_directory) / project.slug / "board.svg"

    def build_board_image(self, project: Project):
        """
        Generate an image displaying the project's board (PCB).
        :param project: Project to have its image created.
        """
        self.driver.export_board_svg(
            str(project.files.board), str(self.board_image_path(project)), project.board_layers
        )

    def build_website(self, projects: list[Project]):
        """
        Build a website based on the given projects.
        :param projects: Projects to be included on the website.
        :return:
        """
        self.build_index(projects)

        for project in projects:
            self.build_project_page(project)

    def build_index(self, projects: list[Project]):
        """Build the website index and write it to the output directory.
        It contains a list of all projects to be showcased.

        :param projects: List of all projects to be shown in the index.
        """
        template = self.environment.get_template("index.html")
        output = self.output_directory / "index.html"

        for project in projects:
            (Path(self.output_directory) / project.slug).mkdir(exist_ok=True)
            self.build_board_image(project)

        with output.open(mode="w", encoding="utf-8") as output_fd:
            output_fd.write(template.render(projects=projects))

    def build_project_page(self, project: Project):
        """Build a project's info page and write it to the output directory.

        :param project: Project where the
        """
        template = self.environment.get_template("board.html")
        (self.output_directory / "boards" / project.slug).with_suffix(".html").write_text(
            template.render(project=project)
        )
