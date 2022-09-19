import pytest
from app import main
from app.config import Config


@pytest.fixture()
def app():
    app = main.app
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def main_url():
    url = "http://127.0.0.1:5000"
    return url
