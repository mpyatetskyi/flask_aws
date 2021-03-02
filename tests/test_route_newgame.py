def test_status_code(data):
    assert data.status_code == 200
    assert data.content_type == 'application/json'


def test_game_id_in_b_response(data):
    assert b'game_id' in data.data
    assert b'cards' in data.data


def test_game_id_in_json_response(data_json):
    assert 'game_id' in data_json


def test_user_cards_in_json_response(data_json):
    assert 'user_cards' in data_json


def test_dealer_cards_in_json_response(data_json):
    assert 'dealer_cards' in data_json


def test_status_in_json_response(data_json):
    assert 'status' in data_json


def test_status_in_range_json_response(data_json):
    assert data_json['status'] in (None, True, False)


def test_game_id_int_in_response_json(data_json):
    assert type(data_json['game_id']) == int


def test_cards_list_in_response_json(data_json):
    assert type(data_json['user_cards']) == list


def test_cards_len_in_response_json(data_json):
    assert type(data_json['user_cards'][0]) == dict
    assert type(data_json['user_cards'][1]) == dict


def test_card_rank_in_range_response_json(data_json):
    assert type(data_json['user_cards'][0]['rank']) == int
    assert data_json['user_cards'][0]['rank'] in range(1, 15)
    assert type(data_json['user_cards'][1]['rank']) == int
    assert data_json['user_cards'][1]['rank'] in range(1, 15)


def test_card_suit_in_range_response_json(data_json):
    assert type(data_json['user_cards'][0]['suit']) == int
    assert data_json['user_cards'][0]['suit'] in range(1, 5)
    assert type(data_json['user_cards'][1]['suit']) == int
    assert data_json['user_cards'][1]['suit'] in range(1, 5)


def test_dealer_cards_list_in_response_json(data_json):
    assert type(data_json['dealer_cards']) == list


def test_dealer_cards_len_in_response_json(data_json):
    assert type(data_json['dealer_cards'][0]) == dict
    assert type(data_json['dealer_cards'][1]) == dict


def test_dealer_card_rank_in_range_response_json(data_json):
    assert type(data_json['dealer_cards'][0]['rank']) == int
    assert data_json['dealer_cards'][0]['rank'] in range(1, 15)
    assert type(data_json['dealer_cards'][1]['rank']) == int
    assert data_json['dealer_cards'][1]['rank'] in range(1, 15)


def test_dealer_card_suit_in_range_response_json(data_json):
    assert type(data_json['user_cards'][0]['suit']) == int
    assert data_json['user_cards'][0]['suit'] in range(1, 5)
