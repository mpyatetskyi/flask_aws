from main import app


def test_status_code():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_game_id_in_b_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    assert b'game_id' in response.data
    assert b'cards' in response.data


def test_game_id_in_json_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert 'game_id' in data


def test_user_cards_in_json_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert 'user_cards' in data


def test_dealer_cards_in_json_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert 'dealer_cards' in data


def test_status_in_json_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert 'status' in data


def test_status_in_range_json_response():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert data['status'] in (None, True, False)


def test_game_id_int_in_response_json():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert type(data['game_id']) == int


def test_cards_list_in_response_json():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert type(data['user_cards']) == list


def test_cards_len_in_response_json():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert type(data['user_cards'][0]) == dict
    assert type(data['user_cards'][1]) == dict


def test_card_rank_in_range_response_json():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert type(data['user_cards'][0]['rank']) == int
    assert data['user_cards'][0]['rank'] in range(1, 15)
    assert type(data['user_cards'][1]['rank']) == int
    assert data['user_cards'][1]['rank'] in range(1, 15)


def test_card_suit_in_range_response_json():
    tester = app.test_client()
    response = tester.get('/newgame')
    data = response.get_json()
    assert type(data['user_cards'][0]['suit']) == int
    assert data['user_cards'][0]['suit'] in range(1, 5)
    assert type(data['user_cards'][1]['suit']) == int
    assert data['user_cards'][1]['suit'] in range(1, 5)
