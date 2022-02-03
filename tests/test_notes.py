from datetime import datetime

from bs4 import BeautifulSoup
import pytest


def _page(data):
    """
    Take the raw HTML for the full page and return a BeautifulSoup object so
    that the tests can check against specific parts of the page.
    """
    return BeautifulSoup(data, "html.parser", from_encoding="utf-8")


def test_redirects(client):
    """These URLs redirect to /view/home."""

    for url in "/view/", "/edit/", "/":
        r = client.get(url)
        assert r.status_code == 302
        assert b'<a href="/view/home">' in r.data


def test_view_page_not_found(client):
    """Viewing a non-existant page returns 404."""

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
    """A missing page body field flashes an error."""

    r = client.post("/edit/test", follow_redirects=True)
    assert _page(r.data).find(class_="alert").string == '"body" field missing!'


def test_markdown_link(client):
    """Rendering of wiki-style links in Markdown."""

    r = client.post("/edit/test", data={"body": "[[link]]"}, follow_redirects=True)
    assert (
        str(_page(r.data).article.p.a)
        == '<a class="internal-link" href="/view/link">link</a>'
    )


def test_markdown_link_alt_title(client):
    """Rendering of wiki links with an alternate title."""

    r = client.post(
        "/edit/test", data={"body": "[[link|alt title]]"}, follow_redirects=True
    )
    assert (
        str(_page(r.data).article.find(class_="internal-link"))
        == '<a class="internal-link" href="/view/link">alt title</a>'
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


def test_url_title_gets_slugified(client):
    """The title in the URL gets slugified."""

    raw_title = "a b-c|d:e=f+g"  # not exhaustive
    for route in ("/view/", "/edit/"):
        r = client.get(route + raw_title)
        print(route)
        assert str(_page(r.data).find(class_="page-title").string) == "a_b_c_d_e_f_g"


def test_page_timestamp(client):
    """The page's timestamp is accurate and rendered correctly."""

    r = client.post("/edit/test", data={"body": "test"}, follow_redirects=True)
    ts_str = str(_page(r.data).find(class_="nav-page-timestamp").string)
    ts_obj = datetime.strptime(ts_str, "Edited: %B %d %Y, %H:%M:%S")
    ts_delta = datetime.now() - ts_obj
    assert ts_delta.seconds <= 5


def test_history_page_not_found(client):
    """Viewing the history of a non-existant page returns 404."""

    r = client.get("/history/no_such_page")
    assert r.status_code == 404
    assert _page(r.data).article.h1.string == "Not Found"


def test_history_bad_revision_redirect(client):
    """A revision that doesn't exist redirects to the history index."""

    client.post("/edit/test", data={"body": "test"})
    r = client.get("/history/test/bad-revision", follow_redirects=True)
    assert r.request.url == 'http://localhost/history/test'


def test_history_revisions(client):
    """Multiple edits of a page create multiple revisions."""

    client.post("/edit/test", data={"body": "revision 1"})
    client.post("/edit/test", data={"body": "revision 2"})
    r = client.get("/history/test")
    assert "Revisions: 2" in str(r.data)
    links = _page(r.data).find(id="revisions").find_all("a")
    for index, anchor_tag in enumerate(reversed(links), start=1):
        rev = client.get(anchor_tag["href"])
        assert _page(rev.data).article.p.string == f"revision {index}"
