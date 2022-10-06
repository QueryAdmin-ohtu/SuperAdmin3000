import pytest

from flask import current_app as flask_app
from initialize_database import initialize_database


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

def pytest_configure():
    initialize_database()
