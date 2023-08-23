# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path

from balba.builder import Builder
from lxml.etree import parse, HTMLParser


def test_builder_dev_mode(tmpdir):
    base_url = "https://my.random.url.test"
    builder = Builder(Path(tmpdir), {"base_url": base_url}, True)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == f"file://{tmpdir}"


def test_builder_no_dev_mode(tmpdir):
    base_url = "https://my.random.url.test"
    builder = Builder(Path(tmpdir), {"base_url": base_url}, False)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == base_url
