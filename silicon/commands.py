import click
from flask.cli import with_appcontext

from silicon.db import db_exists, close_db, init_db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create new tables."""

    if db_exists():
        click.echo("Database already exists.")
    else:
        init_db()
        click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
