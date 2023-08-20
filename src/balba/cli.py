"""CLI Frontend implementation."""
from pathlib import Path

import click
from click import argument, command, option, version_option

from balba import __version__
from balba.balba import balba_run


@command()
@argument("src", type=click.Path(exists=True, file_okay=False))
@option(
    "-o",
    "--output",
    type=click.Path(file_okay=False),
    help="Output folder path",
    default=Path.cwd() / "balba-build",
)
@version_option(__version__)
def balba(*args, **kwargs):
    """Command line entrypoint."""
    raise SystemExit(balba_run(*args, **kwargs))


if __name__ == "__main__":
    balba()
