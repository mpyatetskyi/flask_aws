from flask import Flask, request, jsonify
from methods import card_id, Deck, Ranks, Suits, Card, from_id, GameDataDTO
import sqlite3
from database import User, ChipsLedger, Game, UserCards, DealerCards
import json
from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json
from dataclasses import asdict





app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
conn = sqlite3.connect('blackjack.db', check_same_thread=False)
c = conn.cursor()


@app.route("/")
def hello():
    return jsonify('Hello World')

@app.route("/test")
def tests():
    a ={'game_id' : 1, 'cards' : [{'suit': 'Hearts', 'rank': 'Ace'}, {'suit': 'Spades', 'rank': 'Ace'}]}
    return json.dumps(a)


@app.route('/test/<int:id>', methods=['GET'])
def test(id):
    c.execute('SELECT user_id,chips FROM chips_ledger WHERE user_id=?', [id])
    data = c.fetchall()
    return jsonify(data)


@app.route('/newuser/<string:name>', methods=['GET', 'POST'])
def new_user(name):
    user = User()
    user.insert(name)
    conn.commit()
    data = user.select_user_id()
    return json.dumps(data)

@app.route('/createtables')
def create_tables():
    user = User()
    user.create()
    chips = ChipsLedger()
    chips.create()
    game = Game()
    game.create()
    u_cards = UserCards()
    u_cards.create()
    d_cards = DealerCards()
    d_cards.create()
    conn.commit()
    return "all tables were successfully created"

user_id = 1
deck = Deck()
deck.shuffle()

@app.route('/newgame', methods=['GET', 'POST'])
def new_game():
    user_cards = UserCards()
    dealer_cards = DealerCards()
    game_id = 1
    for _ in range(2):
        user_cards.insert(game_id=game_id, card_id=card_id(deck.deal()))
        dealer_cards.insert(game_id=game_id, card_id=card_id(deck.deal()))
    response = user_cards.select_cards(game_id=game_id)
    gdd = GameDataDTO(game_id=game_id, cards=response, status=None)
    return jsonify(gdd)


@app.route('/decision', methods=['GET', 'POST'] )
def decision():

    game_id = 1
    user_cards = UserCards()
    if request.method == 'GET':
        response = user_cards.select_cards(game_id=game_id)
        return jsonify(game_id=game_id, cards=response)
    elif request.method == 'POST':
        user_cards.insert(game_id=game_id, card_id=card_id(deck.deal()))
        response = user_cards.select_cards(game_id=game_id)
        return jsonify(game_id=game_id, cards=response)


#jsonify(game_id=game_id, suit=card['suit'].name, rank=card['rank'].name)


if __name__ == '__main__':
    app.run(debug=True)