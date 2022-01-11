from datetime import datetime
import string

from flask import current_app

from notes.db import get_db


def read_all():
    """
    Returns all revisions of all pages.
    """
    return get_db().execute('SELECT * FROM pages').fetchall()


def read(title, revision=None):
    """
    Returns a dict with the following items:
    * title (str): the fully-qualified title of the page
    * data (str): the contents of the page's file
    * revision (str): a timestamp of the page's last modification time (or None
        if the page does not exist)

    This returns a dict because that's ultimately the easiest way to get context
    into the Jinja2 templates.
    """
    page = {}

    if revision is None:
        db_row = get_db().execute(
            'SELECT revision, body'
            ' FROM pages'
            ' WHERE title=?'
            ' ORDER BY revision'
            ' DESC'
            ' LIMIT 1',
            (title,)
        ).fetchone()
    else:
        db_row = get_db().execute(
            'SELECT revision, body'
            ' FROM pages'
            ' WHERE title=? AND revision=?'
            ' ORDER BY revision'
            ' DESC'
            ' LIMIT 1',
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
            'INSERT INTO pages'
            ' (revision, title, body) VALUES'
            ' (?, ?, ?)',
            (datetime.now().isoformat(), title, body)
        )
        db.commit()
    except Exception as err:
            current_app.logger.critical(f"Error saving page {title}: {err}'")
            return "Unable to save page"
