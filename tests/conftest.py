import pytest
from main import app


@pytest.fixture(scope="module")
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def connection_newgame(client):
    with client.post('/newgame') as request:
        yield request


@pytest.fixture(scope="module")
def data_json(connection_newgame):
    data = connection_newgame.get_json()
    yield data


@pytest.fixture(scope="module")
def connection_decision(client):
    client.post('/newgame')
    with client.post('/decision') as request:
        yield request


@pytest.fixture(scope="module")
def data_json_decision_post(connection_decision):
    data = connection_decision.get_json()
    yield data
