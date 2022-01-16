from bs4 import BeautifulSoup
import pytest


def _page(data):
    """
    Take the raw HTML for the full page and return a BeautifulSoup object so
    that the tests can check against specific parts of the page.
    """
    return BeautifulSoup(data, "html.parser", from_encoding="utf-8")


def test_redirects(client):
    """These URLs should redirect to /view/home."""

    for url in "/view/", "/edit/", "/":
        r = client.get(url)
        assert r.status_code == 302
        assert b'<a href="/view/home">' in r.data


def test_page_not_found(client):
    """A non-existant page should return 404."""

    r = client.get("/view/no_such_page")
    assert r.status_code == 404
    assert _page(r.data).article.h1.string == "Not Found"


def test_page_add(client):
    """Add a simple page."""

    r = client.post(
        "/edit/test", data={"body": "This is a test"}, follow_redirects=True
    )
    assert r.status_code == 200
    assert _page(r.data).article.p.string == "This is a test"


def test_missing_page_body(client):
    """A missing page body field should flash an error."""

    r = client.post("/edit/test", follow_redirects=True)
    assert _page(r.data).find(id="alert").string == '"body" field missing!'


def test_markdown_link(client):
    """Rendering of wiki-style links in Markdown."""

    r = client.post("/edit/test", data={"body": "[[link]]"}, follow_redirects=True)
    assert (
        str(_page(r.data).article.p.a)
        == '<a class="internal_link" href="/view/link">link</a>'
    )


def test_markdown_link_alt_title(client):
    """Rendering of wiki links with an alternate title."""

    r = client.post(
        "/edit/test", data={"body": "[[link|alt title]]"}, follow_redirects=True
    )
    assert (
        str(_page(r.data).article.find(class_="internal_link"))
        == '<a class="internal_link" href="/view/link">alt title</a>'
    )


def test_markdown_syntax_highlighting(client):
    """Rendering of code block syntax highlighting."""

    code_block_md = '```python\nprint("test")\n```'
    code_block_html = '<div class="highlight"><pre><span></span><span class="nb">print</span><span class="p">(</span><span class="s2">"test"</span><span class="p">)</span></pre></div>'

    r = client.post("/edit/test", data={"body": code_block_md}, follow_redirects=True)
    assert (
        str(_page(r.data).article.find(class_="highlight")).replace("\n", "")
        == code_block_html
    )
