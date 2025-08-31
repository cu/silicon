import json
from pathlib import Path

import click
from flask import current_app

from silicon.page import get_titles, history, read
from silicon.related import get as get_related


def export_db(verbose):
    """
    Export all pages as JSON files to an `export` directory under the instance
    path. Each file has the following structure:

    {
        "title": "some_page_title",
        "attributes": {
            "related": ["example_page", "another_page"],
        "revisions": [
            {
                "timestamp": "2023-11-10T08:02:07.654479",
                "body": "Content of the second revision."
            },
            {
                "timestamp": "2024-05-22T21:27:07.849579",
                "body": "Content of the first revision."
            }
        ]
    }

    This is not optimized for performance (fewest database queries) because
    the intent is to limit memory impact when there are a very large number of
    pages.
    """

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

    # create the export directory
    export_dir = Path(current_app.instance_path) / 'export'
    export_dir.mkdir(exist_ok=True)

    # write each page dict to a JSON file
    for title_row in get_titles():
        title = title_row['title']
        export_file_path = export_dir / f"{title}.json"

        with export_file_path.open('w', encoding='utf-8') as f:
            json.dump(export_page(title), f, ensure_ascii=False, indent=4)
            f.write('\n')

            if verbose:
                click.echo(export_file_path)
