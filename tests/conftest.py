import os
import tempfile

from bs4 import BeautifulSoup
import pytest

from silicon import create_app
from silicon.db import init_db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "test"})

    print(f"Database: {db_path}")

    # create the database and load test data
    with app.app_context():
        init_db()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def page():
    """
    Take the raw HTML for the full page and return a BeautifulSoup object so
    that the tests can check against specific parts of the page.
    """
    def _page(data):
        return BeautifulSoup(data, "html.parser", from_encoding="utf-8")
    return _page
