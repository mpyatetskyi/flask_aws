import pytest
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def data():
    tester = app.test_client()
    request = tester.get('/newgame')
    return request


@pytest.fixture(scope="function")
def data_json(client):
    request = client.get('/newgame')
    data = request.get_json()
    yield data
