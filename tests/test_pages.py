from datetime import datetime


def test_redirects(client):
    """These URLs redirect to /view/home."""

    for url in "/view/", "/edit/", "/":
        r = client.get(url)
        assert r.status_code == 302
        assert b'<a href="/view/home">' in r.data


def test_view_page_not_found(client, page):
    """Viewing a non-existant page returns 404."""

    r = client.get("/view/no_such_page")
    assert r.status_code == 404
    assert page(r.data).article.h1.string == "Not Found"


def test_page_add(client, page):
    """Add a simple page."""

    r = client.post(
        "/edit/test", data={"body": "This is a test"}, follow_redirects=True)
    assert r.status_code == 200
    assert page(r.data).article.p.string == "This is a test"


def test_missing_page_body(client, page):
    """A missing page body field flashes an error."""

    r = client.post("/edit/test", follow_redirects=True)
    assert page(r.data).find(class_="alert").string == '"body" field missing!'


def test_markdown_internal_link(client, page):
    """Rendering of wiki-style links in Markdown."""

    r = client.post(
        "/edit/test", data={"body": "[[link]]"}, follow_redirects=True)
    assert (
        str(page(r.data).article.p.a)
        == '<a class="internal-link" href="/view/link">link</a>')


def test_markdown_internal_link_alt_title(client, page):
    """Rendering of wiki links with an alternate title."""

    r = client.post(
        "/edit/test", data={"body": "[[link|alt title]]"},
        follow_redirects=True)
    assert (
        str(page(r.data).article.find(class_="internal-link"))
        == '<a class="internal-link" href="/view/link">alt title</a>')


def test_markdown_external_link(client, page):
    """External links have a `rel` attribute with 'external' and 'referrer'."""

    r = client.post(
        "/edit/test", data={"body": "http://example.com"},
        follow_redirects=True)
    a_rel = page(r.data).article.p.a['rel']
    assert 'external' in a_rel
    assert 'noreferrer' in a_rel


def test_markdown_syntax_highlighting(client, page):
    """Rendering of code block syntax highlighting."""

    code_block_md = '```python\nprint("test")\n```'
    code_block_html = (
        '<div class="highlight">'
        '<pre>'
        '<span></span>'
        '<span class="nb">print</span>'
        '<span class="p">(</span>'
        '<span class="s2">"test"</span>'
        '<span class="p">)</span>'
        '</pre>'
        '</div>')

    r = client.post(
        "/edit/test", data={"body": code_block_md}, follow_redirects=True)
    assert (
        str(page(r.data).article.find(class_="highlight")).replace("\n", "")
        == code_block_html)


def test_url_title_gets_slugified(client, page):
    """The title in the URL gets slugified."""

    raw_title = "a b-c|d:e=f+g"  # not exhaustive
    for route in ("/view/", "/edit/"):
        r = client.get(route + raw_title)
        print(route)
        assert (
            str(page(r.data).find(class_="page-title").string)
            == "a_b_c_d_e_f_g")


def test_page_timestamp(client, page):
    """The page's timestamp is accurate and rendered correctly."""

    r = client.post("/edit/test", data={"body": "test"}, follow_redirects=True)
    ts_str = str(page(r.data).find(class_="nav-page-timestamp").string)
    ts_obj = datetime.strptime(ts_str, "Edited: %B %d %Y, %H:%M:%S")
    ts_delta = datetime.now() - ts_obj
    assert ts_delta.seconds <= 5


def test_history_page_not_found(client, page):
    """Viewing the history of a non-existant page returns 404."""

    r = client.get("/history/no_such_page")
    assert r.status_code == 404
    assert page(r.data).article.h1.string == "Not Found"


def test_history_bad_revision_redirect(client):
    """A revision that doesn't exist redirects to the history index."""

    client.post("/edit/test", data={"body": "test"})
    r = client.get("/history/test/bad-revision", follow_redirects=True)
    assert r.request.url == 'http://localhost/history/test'


def test_history_revisions(client, page):
    """Multiple edits of a page create multiple revisions."""

    client.post("/edit/test", data={"body": "revision 1"})
    client.post("/edit/test", data={"body": "revision 2"})
    r = client.get("/history/test")
    assert "Revisions: 2" in str(r.data)
    links = page(r.data).find(id="revisions").find_all("a")
    for index, anchor_tag in enumerate(reversed(links), start=1):
        rev = client.get(anchor_tag["href"])
        assert page(rev.data).article.p.string == f"revision {index}"


def test_empty_query(client, page):
    """An empty query displays an error."""

    r = client.get("/search")
    err_msg = page(r.data).find(class_="err-msg").text
    assert r.status_code == 400
    assert err_msg == "No query specified."


def test_search_error(client, page):
    """FTS5 syntax errors are caught and displayed."""

    r = client.get("/search?query=*bar")
    err_msg = page(r.data).find(class_="err-msg").text
    assert r.status_code == 400
    assert err_msg == 'Search Error: fts5: syntax error near "*"'


def test_search_title(client, page):
    """Title is matched in search results."""

    client.post("/edit/alpha_bravo_charlie", data={"body": ""})
    r = client.get("/search?query=bravo")
    title = page(r.data).find(class_="title-matches").text.strip()
    assert title == "alpha_bravo_charlie"


def test_search_body(client, page):
    """Body is matched in search results."""

    client.post("/edit/test", data={"body": "alpha bravo charlie"})
    r = client.get("/search?query=bravo")
    body = page(r.data).find(class_="body-matches").dd.get_text()
    assert body == "alpha bravo charlie"


def test_search_terms_marked(client, page):
    """Matching search terms are marked in title and body."""

    client.post("/edit/hotel_alpha_xray", data={"body": "bravo alpha romeo"})
    r = client.get("/search?query=alpha")
    title_seq = page(r.data).find(class_="title-matches").li.a.contents
    title = ''.join([str(x).strip() for x in list(title_seq)])
    assert title == 'hotel_<mark>alpha</mark>_xray'

    body_seq = page(r.data).find(class_="body-matches").dd.contents
    body = ''.join([str(x) for x in body_seq])
    assert body == 'bravo <mark>alpha</mark> romeo'


def test_search_body_plaintext(client, page):
    """Body snippet does not contain HTML elements."""

    client.post("/edit/test", data={"body": "alpha <b>bravo</b> charlie"})
    r = client.get("/search?query=bravo")
    body = page(r.data).find(class_="body-matches").dd.get_text()
    assert body == "alpha bravo charlie"
