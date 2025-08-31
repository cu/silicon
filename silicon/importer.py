import json
from pathlib import Path

import click
from flask import current_app

from silicon.db import get_db
from silicon.page import write as write_page
from silicon.related import add as add_related


class DbImportError(Exception):
    pass


def import_db(verbose):
    """
    Import pages from JSON files located in an `export` directory under the
    instance path.  If any title/revision pair exists, the body is updated from
    the JSON file. Any errors halt the import process.
    """

    export_dir = Path(current_app.instance_path) / 'export'
    if not export_dir.is_dir():
        raise DbImportError(f"Export directory not found: {export_dir}")

    db = get_db()

    json_files = list(export_dir.glob('*.json'))
    if not json_files:
        raise DbImportError(f"No JSON files found in {export_dir}")

    for json_file in json_files:
        try:
            with json_file.open('r', encoding='utf-8') as f:
                page_data = json.load(f)
        except json.JSONDecodeError as e:
            raise DbImportError(
                f"Error decoding JSON from {json_file.name}: {e}")
        except Exception as e:
            raise DbImportError(f"Error reading {json_file.name}: {e}")

        try:
            title = page_data['title']
            revisions = page_data.get('revisions', [])
            attributes = page_data.get('attributes', {})
            related_pages = attributes.get('related', [])
        except KeyError as e:
            raise DbImportError(
                f"Malformed JSON in {json_file.name}: missing key {e}")

        for revision in revisions:
            write_page(title, revision['body'], revision['timestamp'])

        for related_page in related_pages:
            add_related(title, related_page)

        db.commit()

        if verbose:
            click.echo(json_file.name)
