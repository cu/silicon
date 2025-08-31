import sys

import click

from silicon.db import close_db, db_exists, init_db
from silicon.exporter import export_db
from silicon.importer import DbImportError, import_db


@click.command('init-db')
def init_db_command():
    """Create new tables."""

    if db_exists():
        click.echo("Database already exists.")
    else:
        init_db()
        click.echo("Initialized the database.")


@click.command('export')
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    default=False,
    help="Enable verbose output."
)
def export_db_command(verbose):
    """Export pages as JSON files."""

    if not db_exists():
        click.echo("No database found to export.", err=True)
        sys.exit(1)

    try:
        export_db(verbose)
    except Exception as e:
        click.echo(f"Error exporting database: {e}", err=True)
        sys.exit(1)


@click.command('import')
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    default=False,
    help="Enable verbose output."
)
@click.option(
    '--force',
    '-f',
    is_flag=True,
    default=False,
    help="Overwrite existing pages."
)
def import_db_command(verbose, force):
    """Import pages from JSON files."""

    if db_exists() and not force:
        click.echo("Database exists. Use --force to import anyway.", err=True)
        sys.exit(1)

    if not db_exists():
        init_db()

    try:
        import_db(verbose)
    except DbImportError as e:
        click.echo(e, err=True)
        sys.exit(1)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(export_db_command)
    app.cli.add_command(import_db_command)
