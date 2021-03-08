import sqlite3
from database import User, ChipsLedger, Game, UserCards, DealerCards
from flask import Flask, request, jsonify
from methods import Deck, Card
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
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


@app.route('/newgame', methods=['POST'])
def new_game():
    """Endpoint created to create and start a BlackJack game
    Returns a current game id, player and dealer cards,
    and a game status
    This is using docstrings for specifications.
    ---
    tags:
    - name: "newgame"
    definitions:
      Newgame:
        type: object
        properties:
          game_id:
            type: integer
          user_cards:
            type: array
            items:
              $ref: '#/definitions/Card'
          dealer_card:
            type: array
            items:
              $ref: '#/definitions/Card'
          status:
            type: boolean
      Card:
        type: object
        properties:
          suit:
            type: integer
          rank:
            type: integer
    responses:
      200:
        description: An application/json response
        schema:
          $ref: '#/definitions/Newgame'
        examples:
          newgame: {
            "game_id": 1,
            "user_cards": [{"suit": 1,"rank": 13},
                            {"suit": 4,"rank": 4}],
            "dealer_cards": [{"suit": 1,"rank": 8}],
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
    """Endpoint for user decision (take a card or pass)
        Returns a current game id, player and dealer cards,
        and a game status
        This is using docstrings for specifications.
        ---
      post:
        tags:
        - name: "decision"
          description: ""
        definitions:
          Decision:
            type: object
            properties:
              game_id:
                type: integer
              user_cards:
                type: array
                items:
                  $ref: '#/definitions/Card'
              dealer_card:
                type: array
                items:
                  $ref: '#/definitions/Card'
              status:
                type: boolean
          Card:
            type: object
            properties:
              suit:
                type: integer
              rank:
                type: integer
        responses:
          200:
            description: An application/json response
            schema:
              $ref: '#/definitions/Decision'
            examples:
              newgame: {
                "game_id": 1,
                "user_cards": [{"suit": 1,"rank": 13},
                                {"suit": 4,"rank": 4}],
                "dealer_cards": [{"suit": 1,"rank": 8}],
                "status": null}
      get:
        tags:
        - name: "decision"
          description: ""
        definitions:
          Decision:
            type: object
            properties:
              game_id:
                type: integer
              user_cards:
                type: array
                items:
                  $ref: '#/definitions/Card'
              dealer_card:
                type: array
                items:
                  $ref: '#/definitions/Card'
              status:
                type: boolean
          Card:
            type: object
            properties:
              suit:
                type: integer
              rank:
                type: integer
        responses:
          200:
            description: An application/json response
            schema:
              $ref: '#/definitions/Decision'
            examples:
              newgame: {
                "game_id": 1,
                "user_cards": [{"suit": 1,"rank": 13},{"suit": 4,"rank": 4}],
                "dealer_cards": [{"suit": 1,"rank": 8}],
                "status": null}

        """
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
