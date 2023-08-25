# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path

from lxml.etree import HTMLParser, parse

from balba.builder import Builder
from balba.driver import Driver


def test_builder_dev_mode(tmpdir):
    base_url = "https://my.random.url.test"
    builder = Builder(Path(tmpdir), Driver(False), {"base_url": base_url}, True)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == "/"


def test_builder_no_dev_mode(tmpdir):
    base_url = "https://my.random.url.test/"
    builder = Builder(Path(tmpdir), Driver(False), {"base_url": base_url}, False)
    builder.build_index([])

    tree = parse(str(Path(tmpdir) / "index.html"), HTMLParser())
    legend = tree.xpath("//small[@id='copyright-legend']/a")[0]

    assert legend.attrib["href"] == base_url
