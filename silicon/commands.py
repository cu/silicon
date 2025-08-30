import json
from pathlib import Path
import sys

import click
from flask import current_app

from silicon.db import close_db, db_exists, init_db
from silicon.page import get_titles, history, read
from silicon.related import get as get_related


@click.command('init-db')
def init_db_command():
    """Create new tables."""

    if db_exists():
        click.echo("Database already exists.")
    else:
        init_db()
        click.echo("Initialized the database.")


@click.command('export')
@click.option('--verbose', '-v', is_flag=True, default=False)
def export_db_command(verbose):
    """
    Export all pages as JSON files to an `export` directory under the instance
    path. Each file has the following structure:

    {
        "title": "some-page-title",
        "attributes": {
            "related": ["some_page", "another_page"],
        "revisions": [
            {
                "timestamp": "2023-11-10T08:02:07.654479",
                "body": "Foo bar and/or baz."
            },
            {
                "timestamp": "2024-05-22T21:27:07.849579",
                "body": "Foo bar and/or baz. Oh, and qux."
            }
        ]
    }

    This is not optimized for performance (fewest database queries) because
    the intent is to limit memory impact when there are a very large number of
    pages.
    """

    # if we implement more fancy exporting functionality, move this to
    # its own file, exporters.py
    def export_page(title):
        """
        Export a single page as a dictionary.
        """
        page = {}
        page['title'] = title

        # get attributes
        page['attributes'] = {}
        page['attributes']['related'] = get_related(title)

        # get revisions
        revisions_data = []
        for timestamp in history(title):
            # for each timestamp, read the specific revision of the page
            # and append its timestamp and body to the revisions_data list
            revision_page = read(title, timestamp)
            revisions_data.append({
                "timestamp": revision_page['revision'],
                "body": revision_page['body']
            })
        page['revisions'] = revisions_data

        return page

    if not db_exists():
        click.echo("Database does not exist.")
        sys.exit(1)

    # create the export directory
    export_dir = Path(current_app.instance_path) / 'export'
    export_dir.mkdir(exist_ok=True)

    # write each page dict as a JSON file
    for title_row in get_titles():
        title = title_row['title']
        export_file_path = export_dir / f"{title}.json"
        with export_file_path.open('w', encoding='utf-8') as f:
            json.dump(export_page(title), f, ensure_ascii=False, indent=4)
            f.write('\n')
            if verbose:
                click.echo(export_file_path)



def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(export_db_command)
