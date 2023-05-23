import pytest
from src.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client
