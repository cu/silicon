# This might be a temporary file while I get my bearings on how all this works

import pytest

from notes import create_app
from notes.db import init_db

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'DATABASE': ':memory:'})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'it works' in rv.data
