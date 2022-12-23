from datetime import datetime
import string

from flask import current_app
from sqlite3 import OperationalError

from silicon.db import get_db


class SearchError(Exception):
    pass


def read_all():
    """
    Returns all revisions of all pages.
    """
    return get_db().execute("SELECT * FROM pages").fetchall()


def read(title, revision=None):
    """
    Returns a dict with the following items:
    * title (str): the fully-qualified title of the page
    * body (str): the contents of the page's file
    * revision (str): a timestamp of the page's last modification time (or None
        if the page does not exist)

    This returns a dict because that's ultimately the easiest way to get
    context into the Jinja2 templates.
    """
    page = {}

    if revision is None:
        db_row = get_db().execute(
            "SELECT revision, body "
            "FROM pages "
            "WHERE title=? "
            "ORDER BY revision "
            "DESC "
            "LIMIT 1",
            (title,)
        ).fetchone()
    else:
        db_row = get_db().execute(
            "SELECT revision, body "
            "FROM pages "
            "WHERE title=? AND revision=? "
            "ORDER BY revision "
            "DESC "
            "LIMIT 1",
            (title, revision)
        ).fetchone()

    page = {}
    page['title'] = title
    page['revision'] = None

    if db_row:
        page['revision'] = db_row['revision']
        page['body'] = db_row['body']

    return page


def write(title, body):
    """
    * Write a new revision (title and body) to the database.
    * If there was a problem, return error message.
    """
    try:
        db = get_db()
        db.execute(
            "INSERT INTO pages (revision, title, body) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), title, body)
        )
        db.commit()
    except Exception as err:
        current_app.logger.critical(f"Error saving page {title}: {err}")
        return "Unable to save page"


def history(title):
    """
    Return a list of all revisions of a title.
    """

    revisions = get_db().execute(
        "SELECT revision FROM pages WHERE title=? ORDER BY revision DESC",
        (title,)
    ).fetchall()

    return [r['revision'] for r in revisions]


def search(query):
    """
    Execute a search given a query. Returns a two-element tuple containing
    title results and body results.

    To prevent SQL syntax errors and injection, we replace all non-alpha-
    numeric characters with whitespace except:
    * underscore (_)
    * asterisk (*)
    * plus (+)
    * caret (^)
    * double quotes (", but only an even number)

    These are kept in order to make use of FTS5 query features, although
    there may be some functionality that is lost as a result due to
    characters that I didn't spot in the docs.

    Matching text is surrounded by `__mark__` and `__/mark__` which are then
    substituted for `<mark>` tags via a custom Jinja2 filter.
    """
    def filter_query(query):
        permitted = string.ascii_letters + string.digits + ' _*+^'
        # allow double quotes, but only if there is an even number of them
        if (query.count('"') % 2) == 0:
            permitted += '"'
        filtered = ''
        for char in query:
            if char not in permitted:
                filtered += ' '
            else:
                filtered += char
        return filtered

    filtered_query = filter_query(query)

    try:
        title_results = get_db().execute(
            "SELECT "
            "  title, "
            "  snippet(pages_fts, 0, '__mark__', '__/mark__', '...', 10) "
            "AS snippet "
            "FROM pages_fts "
            "WHERE pages_fts "
            "MATCH ? "
            "ORDER BY rank "
            "LIMIT 50",
            (f'title:{filtered_query}',)
        ).fetchall()

        body_results = get_db().execute(
            "SELECT "
            "  title, "
            "  snippet(pages_fts, 1, '__mark__', '__/mark__', '...', 64) "
            "AS snippet "
            "FROM pages_fts "
            "WHERE pages_fts "
            "MATCH ? "
            "ORDER BY rank "
            "LIMIT 50",
            (f"body:{filtered_query}",)
        ).fetchall()
    except OperationalError as err:
        raise SearchError(f"Search Error: {err}")

    return title_results, body_results
