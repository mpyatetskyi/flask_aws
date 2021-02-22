from main import app


def test_index():
    tester = app.test_client()
    response = tester.get("/")
    assert response.status_code == 200


# Check if content is application/json
def test_index_content():
    tester = app.test_client()
    response = tester.get("/", content_type='application/json')
    assert response.content_type == 'application/json'


# Check for data returned
def test_index_data():
    tester = app.test_client()
    response = tester.get("/")
    assert b'Hello World' in response.data


def test_new_game_index():
    tester = app.test_client()
    response = tester.get("/newgame")
    assert response.status_code == 200


def test_new_game_content():
    tester = app.test_client()
    response = tester.get("/newgame", content_type='application/json')
    assert response.content_type == 'application/json'


def test_new_game():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert response.json
