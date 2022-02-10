import click
from flask.cli import with_appcontext

from notes.db import close_db, init_db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create new tables."""

    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
