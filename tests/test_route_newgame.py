def test_status_code_and_content(connection):
    assert connection.status_code == 200
    assert connection.content_type == 'application/json'


def test_keys_data_types_in_response_json(data_json):
    assert type(data_json['game_id']) == int
    assert type(data_json['user_cards']) == list
    assert type(data_json['dealer_cards']) == list
    assert data_json['status'] in (None, True, False)


def test_cards_type_response_json(data_json):
    data = data_json['user_cards'] + data_json['dealer_cards']
    assert all([type(a) == dict for a in data])


def test_cards_in_response_json(data_json):
    assert all([card['rank'] in range(1, 15) for
                card in data_json['user_cards']])
    assert all([card['rank'] in range(1, 15) for
                card in data_json['dealer_cards']])
    assert all([card['suit'] in range(1, 5) for
                card in data_json['user_cards']])
    assert all([card['suit'] in range(1, 5) for
                card in data_json['dealer_cards']])
