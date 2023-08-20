"""Layer that interacts with the kicad-cli executable."""
from subprocess import CalledProcessError, run


class Driver:
    """Component in charge of communicating the application code with the kicad-cli executable."""

    @staticmethod
    def version() -> str:
        """Version of the available (must be in PATH) kicad-cli executable."""
        try:
            result = run(["kicad-cli", "version"], capture_output=True, check=True)
            return result.stdout.decode("utf-8")
        except (CalledProcessError, FileNotFoundError):
            return ""

    @staticmethod
    def export_schematic(src: str, dst: str) -> int:
        """
        Export a schematic to a PDF file.
        :param src: path to the schematic
        :param dst: output path (and name)
        :return: return code as provided by kicad-cli
        """
        return run(["kicad-cli", "sch", "export", "pdf", "--output", dst, src], check=False).returncode

    @staticmethod
    def export_board(src: str, dst: str, layers: list[str]) -> int:
        """
        Export a board to an image file.
        :param src:
        :param dst:
        :param layers:
        :return:
        """
        return run(
            [
                "kicad-cli",
                "board",
                "export",
                "pdf",
                "--layers",
                ",".join(layers),
                "--output",
                dst,
                src,
            ],
            check=False,
        ).returncode
