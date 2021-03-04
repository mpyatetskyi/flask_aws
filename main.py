import sqlite3
from database import User, ChipsLedger, Game, UserCards, DealerCards
from flask import Flask, request, jsonify
from methods import Deck, Card


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
database_link = 'C:/Users/mpiatetskyi/PycharmProjects/flask_aws/blackjack.db'
conn = sqlite3.connect(database_link, check_same_thread=False)
c = conn.cursor()


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


@app.route('/newgame', methods=['GET', 'POST'])
def new_game():
    """Example endpoint creates a new game and
        returns a current game id, user and dealer cards
        and a game status checking if there is a winner
        This is using json for specifications.
        ---
        definitions:
          GameDefinitionObject:
            type: object
              properties:
                game_id:
                  type: integer
                user_cards:
                  type: array
                  items:
                    $ref: '#/definitions/Card'
                dealer_cards:
                  type: array
                  items:
                    $ref: '#/definitions/Card'
                status:
                  type: bool
          Card:
            type: object
              properties:
                suit:
                  type: IntEnum
                rank:
                  type: IntEnum

        responses:
          200:
            description: A json object
            schema:
              $ref: '#/definitions/GameDefinitionObject'
            examples:
              rgb: {"game_id": 1,"user_cards": [{"suit": 3,"rank": 5},
                    {"suit": 3,"rank": 13}],
                    "dealer_cards": [{"suit": 3,"rank": 2}],
                    "status": null}
        """
    game_id = 1

    dealer_cards = DealerCards()
    user_cards = UserCards()
    for _ in range(2):
        user_cards.insert(game_id=game_id, card_id=deck.deal().to_id())
        dealer_cards.insert(game_id=game_id, card_id=deck.deal().to_id())
    user = user_cards.select_cards(game_id=game_id)
    dealer = dealer_cards.select_one_card(game_id=game_id)
    conn.commit()
    return jsonify(game_id=game_id, user_cards=user,
                   dealer_cards=dealer, status=None)


game_id = 1


@app.route('/decision', methods=['GET', 'POST'])
def decision():
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
