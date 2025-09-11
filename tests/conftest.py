import shutil

from bs4 import BeautifulSoup
import pytest

from silicon import create_app
from silicon.db import init_db


@pytest.fixture
def app():
    """Create a new app instance for each test."""
    app = create_app(testing=True)
    with app.app_context():
        init_db()
    yield app

    shutil.rmtree(app.instance_path)


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
