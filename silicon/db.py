import sqlite3

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        # return rows that behave like dicts
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def db_exists():
    """
    Check to see if the database has been initialized, using the existence of
    the `pages` table as a proxy.
    """
    result = get_db().execute(
        "SELECT name"
        " FROM sqlite_master"
        " WHERE type='table'"
        "  AND name='pages'"
    ).fetchone()
    if result is not None and result[0] == 'pages':
        return True
