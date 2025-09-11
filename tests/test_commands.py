from datetime import datetime
import json
import os

from silicon import page
from silicon.related import add as add_related
from silicon.related import get as get_related


def test_export_command(app, runner):
    """
    Tests the basic functionality of the 'export' command.
    It creates a page, runs export, and verifies the output file.
    """
    revision = datetime.now().isoformat()
    with app.app_context():
        page.write('export_page', 'This is the body.', revision=revision)
        add_related('export_page', 'related_page_a')
        add_related('export_page', 'related_page_b')
        result = runner.invoke(args=['export'])
    assert result.exit_code == 0, result.output

    export_dir = os.path.join(app.instance_path, 'export')
    exported_file = os.path.join(export_dir, 'export_page.json')
    assert os.path.exists(exported_file)

    with open(exported_file) as f:
        data = json.load(f)

    assert data['title'] == 'export_page'
    assert len(data['revisions']) == 1
    assert data['revisions'][0]['body'] == 'This is the body.'
    assert data['revisions'][0]['revision'] == revision
    assert 'related_page_a' in data['attributes']['related']
    assert 'related_page_b' in data['attributes']['related']


def test_import_fails_if_db_exists_without_force(app, runner):
    """
    Tests that import command fails if the database exists
    and --force is not used.
    """
    export_dir = os.path.join(app.instance_path, 'export')
    os.makedirs(export_dir, exist_ok=True)
    import_file = os.path.join(export_dir, 'dummy.json')
    with open(import_file, 'w') as f:
        json.dump({"title": "dummy", "revisions": []}, f)

    result = runner.invoke(args=['import'])
    assert result.exit_code != 0


def test_import_command(app, runner):
    """
    Tests the basic functionality of the 'import' command.
    It creates a JSON file and runs import, then verifies the page was created.
    """
    export_dir = os.path.join(app.instance_path, 'export')
    os.makedirs(export_dir, exist_ok=True)
    import_file = os.path.join(export_dir, 'import_page.json')
    revision = datetime.now().isoformat()

    import_data = {
        'title': 'import_page',
        'attributes': {
            'related': ['related_page_a', 'related_page_b']
        },
        'revisions': [
            {
                'revision': revision,
                'body': 'Imported body.'
            }
        ]
    }
    with open(import_file, 'w') as f:
        json.dump(import_data, f)

    with app.app_context():
        result = runner.invoke(args=['import', '--force'])
        assert result.exit_code == 0, result.output
        imported_page = page.read('import_page')
        related = get_related('import_page')

    assert imported_page['title'] == 'import_page'
    assert imported_page['body'] == 'Imported body.'
    assert imported_page['revision'] == revision
    assert 'related_page_a' in related
    assert 'related_page_b' in related


def test_round_trip(app, runner):
    """
    Tests that exporting and then importing a page preserves its content,
    especially with tricky characters.
    """
    title = 'tricky_content_page'
    body = """
    Here's some "tricky" content.
    'Single quotes' are here.
    <Tags> and [brackets] and {braces}.
    Unicode: \u2603 SNOWMAN

    Leading and trailing whitespace.

    """
    revision = datetime.now().isoformat()

    with app.app_context():
        page.write(title, body, revision=revision)
        original_page = page.read(title)
        result = runner.invoke(args=['export'])
        assert result.exit_code == 0, result.output

    os.remove(os.path.join(app.instance_path, 'silicon.sqlite'))

    with app.app_context():
        result = runner.invoke(args=['import'])
        assert result.exit_code == 0, result.output
        round_tripped_page = page.read(title)

    assert round_tripped_page['title'] == original_page['title']
    assert round_tripped_page['body'] == original_page['body']
    assert round_tripped_page['revision'] == original_page['revision']


def test_import_upsert(app, runner):
    """
    Tests that importing a page with two identical revision strings works, and
    uses the most recent body version presented. (This tests the upsert
    functionality in page.py.)
    """
    export_dir = os.path.join(app.instance_path, 'export')
    os.makedirs(export_dir, exist_ok=True)
    import_file = os.path.join(export_dir, 'import_page.json')
    revision = datetime.now().isoformat()

    import_data = {
        'title': 'import_page',
        'revisions': [
            {
                'revision': revision,
                'body': 'First imported body.'
            },
            {
                'revision': revision,
                'body': 'Second imported body.'
            }
        ]
    }
    with open(import_file, 'w') as f:
        json.dump(import_data, f)

    with app.app_context():
        result = runner.invoke(args=['import', '--force'])
        assert result.exit_code == 0, result.output
        imported_page = page.read('import_page')

    assert imported_page['title'] == 'import_page'
    assert imported_page['body'] == 'Second imported body.'
    assert imported_page['revision'] == revision


def test_export_fails_if_no_db(app, runner):
    """Tests that export command fails if the database does not exist."""
    db_path = os.path.join(app.instance_path, 'silicon.sqlite')
    if os.path.exists(db_path):
        os.remove(db_path)

    result = runner.invoke(args=['export'])
    assert result.exit_code != 0


def test_import_with_malformed_json(app, runner):
    """Tests that import command handles malformed JSON files gracefully."""
    export_dir = os.path.join(app.instance_path, 'export')
    os.makedirs(export_dir, exist_ok=True)
    import_file = os.path.join(export_dir, 'malformed.json')

    with open(import_file, 'w') as f:
        f.write('{"title": "malformed", "revisions": [')  # Incomplete JSON

    db_path = os.path.join(app.instance_path, 'silicon.sqlite')
    if os.path.exists(db_path):
        os.remove(db_path)

    result = runner.invoke(args=['import'])
    assert result.exit_code != 0
