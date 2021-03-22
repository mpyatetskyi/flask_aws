import sqlite3
import bcrypt
import jwt
import datetime
from database import User, ChipsLedger, Game, UserCards, DealerCards
from flasgger import Swagger
from flask import Flask, request, jsonify, make_response
from functools import wraps
from methods import Deck, Status


app = Flask(__name__)
swagger = Swagger(app)
app.config['JSON_SORT_KEYS'] = False
database_link = 'C:/Users/mpiatetskyi/PycharmProjects/flask_aws/blackjack.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = database_link
conn = sqlite3.connect(database_link, check_same_thread=False)
c = conn.cursor()


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            c.execute('SELECT * FROM user WHERE user_id=? LIMIT 1', [data['user_id']])
            user = c.fetchone()
            current_user = user[0]

        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/test')
@token_required
def test(current_user):
    return jsonify({"user_id": current_user})


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


@app.route('/signup', methods=['POST'])
def sign_up():
    """
    Create a new user
    ---
    tags:
    - name: "user"
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
    - in: body
      name: user
      description: The user to create
      schema:
        $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        required:
          - name
          - email
          - password
        properties:
          name:
            type: string
          email:
            type: string
          password:
            type: string
    responses:
      default:
        description: successful operation

        """

    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'Name is missing!'})

    elif 'email' not in data:
        return jsonify({'message': 'Email is missing!'})

    elif 'password' not in data:
        return jsonify({'message': 'Password is missing!'})

    elif all(data[i] for i in ['name', 'email', 'password']):

        user = User()
        name = data['name']
        email = data['email']
        password = bcrypt.hashpw(data['password'].encode('utf-8'),
                                 bcrypt.gensalt(10)).decode('utf-8')

        if user.select_user_by_email(email):
            return jsonify({'message': 'User with such email already exist'})

        user.insert(name, email, password)
        conn.commit()

        return jsonify({'message': 'New user created!'})


@app.route('/login')
def login():
    auth = request.get_json()

    if 'email' not in auth or 'password' not in auth:
        return make_response('Could not verify', 401,
                             {'WWW-Authenticate':
                              'Basic realm="Login required!"'})

    c.execute('SELECT user_name FROM user WHERE email=? LIMIT 1',
              [auth['email']])
    user = c.fetchone()[0]

    if not user:
        return make_response('Could not verify', 401,
                             {'WWW-Authenticate':
                              'Basic realm="Login required!"'})

    c.execute('SELECT password FROM user WHERE email=?', [auth['email']])
    pwd = c.fetchone()[0]

    c.execute('SELECT user_id FROM user WHERE email=?', [auth['email']])
    id = c.fetchone()[0]

    if bcrypt.checkpw(auth["password"].encode('utf-8'), pwd.encode('UTF-8')):
        token = jwt.encode({"user_id": id,
                            'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({"token": token})

    return make_response('Could not verify', 401,
                         {'WWW-Authenticate':
                          'Basic realm="Login required!"'})


@app.route('/logout', methods=['POST'])
def logout():
    pass


user_id = 1


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
          user_points:
            type: integer
          dealer_card:
            type: array
            items:
              $ref: '#/definitions/Card'
          dealer_points:
            type: integer
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

    deck = Deck()
    game_id = 1

    dealer_cards = DealerCards()
    user_cards = UserCards()
    for _ in range(2):
        user_cards.insert(game_id=game_id, card_id=deck.deal().to_id())
        dealer_cards.insert(game_id=game_id, card_id=deck.deal().to_id())
    user = user_cards.select_cards(game_id=game_id)
    dealer = dealer_cards.select_one_card(game_id=game_id)
    conn.commit()
    status = Status.status_check(user)
    user_value = Status.cards_value(user)
    dealer_value = Status.cards_value(dealer)
    return jsonify(game_id=game_id, user_cards=user,
                   user_points=user_value, dealer_cards=dealer,
                   dealer_points=dealer_value, status=status)


@app.route('/decision', methods=['GET', 'POST'])
def decision():
    """Endpoint for user decision (take a card or pass)
        Returns a current game id, player and dealer cards,
        and a game status
        This is using docstrings for specifications.
        ---
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
              user_points:
                type: integer
              dealer_card:
                type: array
                items:
                  $ref: '#/definitions/Card'
              dealer_points:
                type: integer
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
                "user_points": 14,
                "dealer_cards": [{"suit": 1,"rank": 8}],
                "dealer_points": 0,
                "status": null}
        """

    game_id = 1
    user_cards = UserCards()
    dealer_cards = DealerCards()

    cards = (user_cards.select_cards(game_id=game_id) +
             dealer_cards.select_cards(game_id=game_id))
    deck = Deck.recreate_deck(cards=cards)

    if request.method == 'POST':
        user_cards.insert(game_id=game_id, card_id=deck.deal().to_id())
        conn.commit()
        user = user_cards.select_cards(game_id=game_id)
        dealer = dealer_cards.select_one_card(game_id=game_id)
        status = Status.status_check(user)
        user_value = Status.cards_value(user)
        dealer_value = Status.cards_value(dealer)

        return jsonify(game_id=game_id, user_cards=user,
                       user_points=user_value, dealer_cards=dealer,
                       dealer_points=dealer_value, status=status)

    elif request.method == 'GET':
        points = Status.cards_value(
            dealer_cards.select_cards(game_id=game_id))
        while points < 17:
            dealer_cards.insert(game_id=game_id,
                                card_id=deck.deal().to_id())
            conn.commit()
            points = Status.cards_value(
                dealer_cards.select_cards(game_id=game_id))

        user = user_cards.select_cards(game_id=game_id)
        dealer = dealer_cards.select_cards(game_id=game_id)
        user_value = Status.cards_value(user)
        dealer_value = Status.cards_value(dealer)
        status = Status.status_check(user, dealer_value=dealer)

        return jsonify(game_id=game_id, user_cards=user,
                       user_points=user_value, dealer_cards=dealer,
                       dealer_points=dealer_value, status=status)


@app.route('/chips', methods=['GET'])
@token_required
def get_chips(current_user):
    chips = ChipsLedger()
    total = chips.select_total_chips(current_user)
    if total is None:
        return jsonify(chips=0)
    return jsonify(chips=total)


@app.route('/chips/<cash>', methods=['POST'])
@token_required
def add_chips(current_user, cash):
    chips = ChipsLedger()
    chips.insert(current_user, cash)
    return jsonify({"message": str(cash) + "$ added"})


if __name__ == '__main__':
    app.run(debug=True)
