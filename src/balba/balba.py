"""Implementation of the program's workflow"""
from click import echo, style

from balba.driver import Driver


def balba_run(src: str, output: str) -> int:
    """Perform the website building process."""
    version = Driver.version()
    if not version:
        echo(style("Could not find a valid kicad-cli version", fg="red"))
        return 127

    echo(f"Using kicad-cli {version}")
    echo(f"Looking for Kicad projects in {src}")
    # TODO: Collect all kicad_pro files

    echo(f"Generating website in {output}")

    return 0
