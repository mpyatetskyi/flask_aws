def test_status_code_and_content(connection):
    assert connection.status_code == 200
    assert connection.content_type == 'application/json'


def test_keys_json_response(data_json):
    expectation = ['game_id', 'user_cards',
                   'dealer_cards', 'status']
    assert all([a in data_json for a in expectation])


def test_data_types_in_response_json(data_json):
    assert type(data_json['game_id']) == int
    assert type(data_json['user_cards']) == list
    assert type(data_json['dealer_cards']) == list


def test_status_json_response(data_json):
    assert data_json['status'] in (None, True, False)


def test_cards_type_response_json(data_json):
    assert all([type(a) == dict for a in data_json['user_cards']])
    assert all([type(a) == dict for a in data_json['dealer_cards']])


def test_card_rank_in_response_json(data_json):
    assert all([type(card['rank']) == int for
                card in data_json['user_cards']])
    assert all([type(card['rank']) == int for
                card in data_json['dealer_cards']])
    assert all([card['rank'] in range(1, 15) for
                card in data_json['user_cards']])
    assert all([card['rank'] in range(1, 15) for
                card in data_json['dealer_cards']])


def test_card_suit_in_range_response_json(data_json):
    assert all([type(card['suit']) == int for
                card in data_json['user_cards']])
    assert all([type(card['suit']) == int for
                card in data_json['dealer_cards']])
    assert all([card['suit'] in range(1, 5) for
                card in data_json['user_cards']])
    assert all([card['suit'] in range(1, 5) for
                card in data_json['dealer_cards']])
