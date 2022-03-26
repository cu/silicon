import pytest


def test_add_relationship(client, page):
    """Add relationship between pages."""

    r = client.post("/related/foo", data={"relative": "Test Rel 1"})
    assert page(r.data).li.a.string.strip() == "test_rel_1"
    r = client.get("/related/test_rel_1")
    assert page(r.data).li.a.string.strip() == "foo"


def test_delete_relationship(client, page):
    """Remove a relationship between pages."""

    client.post("/related/foo", data={"relative": "bar"})
    r = client.post("/related/foo", data={"relative": "baz"})
    relatives = [li.a.string.strip() for li in page(r.data).ul.find_all("li")]
    assert relatives == ['bar', 'baz']

    r = client.delete("/related/foo/baz")
    relatives = [li.a.string.strip() for li in page(r.data).ul.find_all("li")]
    assert relatives == ['bar']


def test_self_relationship_fails(client, page):
    """Page cannot be related to itself."""

    r = client.post("/related/foo", data={"relative": "foo"})
    assert page(r.data).ul.li is None


def test_duplicate_relationships_fail(client, page):
    """Duplicate relationships are not added."""

    client.post("/related/foo", data={"relative": "bar"})
    r = client.post("/related/foo", data={"relative": "bar"})
    relatives = [li.a.string.strip() for li in page(r.data).ul.find_all("li")]
    assert relatives == ['bar']


def test_empty_relationship_fails(client, page):
    """Empty relationships are not added."""

    client.post("/related/foo", data={"relative": "bar"})
    r = client.post("/related/foo", data={"relative": ""})
    relatives = [li.a.string.strip() for li in page(r.data).ul.find_all("li")]
    assert relatives == ['bar']
