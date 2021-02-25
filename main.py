import json
import sqlite3
from database import User, ChipsLedger, Game, UserCards, DealerCards
from flask import Flask, request, jsonify
from methods import Deck, Card


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
conn = sqlite3.connect('blackjack.db', check_same_thread=False)
c = conn.cursor()


@app.route("/")
def hello():
    return jsonify('Hello World')


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
    game_id = 1
    user_cards = UserCards()
    dealer_cards = DealerCards()
    for _ in range(2):
        user_cards.insert(game_id=game_id, card_id=Card.to_id(deck.deal()))
        dealer_cards.insert(game_id=game_id, card_id=Card.to_id(deck.deal()))
    user = user_cards.select_cards(game_id=game_id)
    dealer = dealer_cards.select_one_card(game_id=game_id)
    return jsonify(game_id=game_id, user_cards=user,
                   dealer_cards=dealer, status=None)


@app.route('/decision', methods=['GET', 'POST'])
def decision():

    game_id = 1
    user_cards = UserCards()
    if request.method == 'GET':
        response = user_cards.select_cards(game_id=game_id)
        return jsonify(game_id=game_id, cards=response)
    elif request.method == 'POST':
        user_cards.insert(game_id=game_id, card_id=Card.to_id((deck.deal())))
        response = user_cards.select_cards(game_id=game_id)
        return jsonify(game_id=game_id, cards=response)


if __name__ == '__main__':
    app.run(debug=True)
