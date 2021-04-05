def test_status_code_and_content(connection_decision):
    assert connection_decision.status_code == 200
    assert connection_decision.content_type == 'application/json'


def test_keys_data_types_in_response_json(data_json_decision_post):
    assert type(data_json_decision_post['game_id']) == int
    assert type(data_json_decision_post['user_cards']) == list
    assert type(data_json_decision_post['dealer_cards']) == list
    assert data_json_decision_post['status'] in (None, True, False)
    assert type(data_json_decision_post['user_points']) == int
    assert type(data_json_decision_post['dealer_points']) == int
