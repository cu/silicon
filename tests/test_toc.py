from pathlib import Path

import pytest


def test_table_of_contents(client):
    """Generation of a table of contents for a page."""

    toc_in = Path(__file__).parent / "toc_in.md"
    toc_out = Path(__file__).parent / "toc_out.html"
    with toc_in.open() as f:
        r = client.post("/toc", data={"body": f.read()})
    with toc_out.open() as f:
        assert r.data.decode("utf-8") == f.read()
