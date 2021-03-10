import pytest
from main import app


@pytest.fixture(scope="module")
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def connection(client):
    with client.get('/newgame') as request:
        yield request


@pytest.fixture(scope="module")
def data_json(connection):
    data = connection.get_json()
    yield data
