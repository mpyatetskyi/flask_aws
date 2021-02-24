from main import app


def test_status_code():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_game_id_in_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert b'game_id' in response.data


def test_cards_in_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert b'cards' in response.data


