import sqlite3
import bcrypt
import jwt
import datetime
from database import User, ChipsLedger, Game, UserCards, DealerCards
from flasgger import Swagger
from flask import Flask, request, jsonify, make_response
from functools import wraps
from methods import Deck, Status
from send_email import send_email


app = Flask(__name__)
app.config.update(
    JSON_SORT_KEYS=False,
    SECRET_KEY='secret',
    SQLALCHEMY_DATABASE_URI='C:/Users/mpiatetskyi/PycharmProjects/'
                            'flask_aws/blackjack.db',
    SWAGGER={
        "title": 'My API',
        "uiversion": 3,
        "specs_route": "/apidocs/"
    }
)

conn = sqlite3.connect('C:/Users/mpiatetskyi/PycharmProjects/'
                       'flask_aws/blackjack.db', check_same_thread=False)
c = conn.cursor()


template = {
  "swagger": "2.0",
  "info": {
    "title": "Flask Restful BlackJack game API",
    "description": "This is a swagger documentation made "
                   "by Maksym Piatetskyi for DA internship project",
    "version": "0.0.1",
    "contact": {
      "name": "Maksym Piatetskyi",
      "url": "https://www.linkedin.com/in/maksym-piatetskyi-4960b47a/",
      "email": "m.pyatetskyi@gmail.com"
    }
  },
  "securityDefinitions": {
    "Bearer": {
        "type": "apiKey",
        "name": "x-access-token",
        "in": "header",
        "description": "JWT Authorization header using the Bearer scheme."
                       " Example: \"x-access-token: {token}\""
    }
  },
  "security": [
    {
      "Bearer": []
    }
  ]
}


swagger = Swagger(app, template=template)


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms='HS256')
            c.execute('SELECT * FROM user WHERE user_id=? LIMIT 1',
                      [data['user_id']])
            user = c.fetchone()
            current_user = user[0]

        except TypeError:
            return jsonify({'message': 'Token is invalid'}), 401
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/signup', methods=['POST'])
def sign_up():
    """
    User to signup
    ---
      tags:
        - user
      summary: Create user
      description:
      consumes:
        - application/json
      produces:
        - application/json
      parameters:
        - in: body
          name: body
          description: Created user object
          required: true
          schema:
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


@app.route('/login', methods=['POST'])
def login():
    """
    User to login
    ---
      tags:
        - user
      summary: User to login
      description:
      consumes:
        - application/json
      produces:
        - application/json
      parameters:
        - in: body
          name: body
          description: Created user object
          required: true
          schema:
            properties:
              email:
                type: string
              password:
                type: string
      responses:
        '200':
          description: successful operation
          schema:
            properties:
              token:
                type: string
    """
    auth = request.get_json()

    if 'email' not in auth or 'password' not in auth:
        return make_response('Could not verify', 401,
                             {'WWW-Authenticate':
                              'Basic realm="Login required!"'})

    try:
        c.execute('SELECT user_name FROM user WHERE email=? LIMIT 1',
                  [auth['email']])
        user = c.fetchone()[0]
    except TypeError:
        return jsonify({'message': 'Wrong email or password'}), 400

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


@app.route("/delete", methods=["DELETE"])
@token_required
def delete_user(current_user):
    """
    User to delete his account
    This can only be done by the logged in user.
    Token required

    ---
      tags:
        - user
      summary: User to delete his account
      description:
      consumes:
        - application/json
      produces:
        - application/json
      responses:
        '200':
          description: successful operation

    """
    user = User()
    user.delete_user(current_user)
    return jsonify({"message": "User was successfully deleted"})


@app.route('/newgame', methods=['POST'])
@token_required
def new_game(current_user):
    """
        Start a new game
        This can only be done by the logged in user.
        Token required
        ---
        tags:
        - name: "game"
          description: ""
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
        - in: body
          name: bet
          description: User to make a bet before start a new BlackJack game
          required: true
          schema:
            properties:
              bet:
                type: integer
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
              bet:
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
                "bet": 20,
                "status": null}
        """

    data = request.get_json()

    if 'bet' not in data:
        return {'message': 'Please make a bet'}

    elif data["bet"] < 0:
        return {'message': 'Bet cant be negative '}

    bet = int(data['bet'])

    chips = ChipsLedger()

    if not chips.select_total_chips(current_user):
        return jsonify({'message': 'You have no money in your wallet to play'})

    if bet > chips.select_total_chips(current_user):
        return jsonify({'message': 'You don`t have enough money'
                                   ' to make a bet!'})

    deck = Deck()
    game = Game()

    game.insert(current_user, bet)

    game_id = game.select_game_id(current_user)
    dealer_cards = DealerCards()
    user_cards = UserCards()
    for _ in range(2):
        user_cards.insert(game_id=game_id[0], card_id=deck.deal().to_id())
        dealer_cards.insert(game_id=game_id[0], card_id=deck.deal().to_id())
    user = user_cards.select_cards(game_id=game_id[0])
    dealer = dealer_cards.select_one_card(game_id=game_id[0])
    conn.commit()
    status = Status.status_check(user)
    user_value = Status.cards_value(user)
    dealer_value = Status.cards_value(dealer)
    return jsonify(game_id=game_id, user_cards=user,
                   user_points=user_value, dealer_cards=dealer,
                   dealer_points=dealer_value, bet=bet, status=status)


@app.route('/decision', methods=['GET'])
@token_required
def dealer_turn_decision(current_user):
    """
    User decides not to take a card!
    Starts dealers turn.
    This can only be done by the logged in user.
    Token required
    ---
        tags:
        - name: "game"
          description: ""
        produces:
        - application/json
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
              bet:
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
              response: {
                "game_id": 1,
                "user_cards": [{"suit": 1,"rank": 13},
                                {"suit": 4,"rank": 4}],
                "user_points": 14,
                "dealer_cards": [{"suit": 1,"rank": 8}],
                "dealer_points": 0,
                "bet": 20,
                "status": null,
                }

        """

    game = Game()
    game_id = game.select_game_id(current_user)
    bet = game.select_bet(current_user, game_id[0])
    user_cards = UserCards()
    dealer_cards = DealerCards()

    cards = (user_cards.select_cards(game_id=game_id[0]) +
             dealer_cards.select_cards(game_id=game_id[0]))
    deck = Deck.recreate_deck(cards=cards)

    points = Status.cards_value(
        dealer_cards.select_cards(game_id=game_id[0]))
    while points < 17:
        dealer_cards.insert(game_id=game_id[0],
                            card_id=deck.deal().to_id())
        conn.commit()
        points = Status.cards_value(
            dealer_cards.select_cards(game_id=game_id[0]))

    user = user_cards.select_cards(game_id=game_id[0])
    dealer = dealer_cards.select_cards(game_id=game_id[0])
    user_value = Status.cards_value(user)
    dealer_value = Status.cards_value(dealer)
    status = Status.status_check(user, dealer_value=dealer)

    return jsonify(game_id=game_id[0], user_cards=user,
                   user_points=user_value, dealer_cards=dealer,
                   dealer_points=dealer_value, bet=bet, status=status)


@app.route('/decision', methods=['POST'])
@token_required
def take_card_decision(current_user):
    """
    User decides to take a card!
    Users turn.
    This can only be done by the logged in user.
    Token required
    ---
        tags:
        - name: "game"
          description: ""
        produces:
        - application/json
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
              bet:
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
              response: {
                "game_id": 1,
                "user_cards": [{"suit": 1,"rank": 13},
                                {"suit": 4,"rank": 4}],
                "user_points": 14,
                "dealer_cards": [{"suit": 1,"rank": 8}],
                "dealer_points": 0,
                "bet": 20,
                "status": null,
                }

        """

    game = Game()
    game_id = game.select_game_id(current_user)
    bet = game.select_bet(current_user, game_id[0])
    user_cards = UserCards()
    dealer_cards = DealerCards()

    cards = (user_cards.select_cards(game_id=game_id[0]) +
             dealer_cards.select_cards(game_id=game_id[0]))
    deck = Deck.recreate_deck(cards=cards)

    user_cards.insert(game_id=game_id[0], card_id=deck.deal().to_id())
    conn.commit()
    user = user_cards.select_cards(game_id=game_id[0])
    dealer = dealer_cards.select_one_card(game_id=game_id[0])
    status = Status.status_check(user)
    user_value = Status.cards_value(user)
    dealer_value = Status.cards_value(dealer)

    return jsonify(game_id=game_id[0], user_cards=user,
                   user_points=user_value, dealer_cards=dealer,
                   dealer_points=dealer_value, bet=bet[0], status=status)


@app.route('/winner', methods=["GET"])
@token_required
def winner(current_user):
    """
    Choose a winner
    This can only be done by the logged in user.
    Token required
    ---
        tags:
        - name: "game"
          description: ""
        produces:
        - application/json
        responses:
          200:
            description: An application/json response
    """
    game = Game()
    game_id = game.select_game_id(current_user)
    bet = game.select_bet(current_user, game_id[0])
    bet = int(bet[0])
    user_cards = UserCards()
    dealer_cards = DealerCards()
    user = user_cards.select_cards(game_id=game_id[0])
    dealer = dealer_cards.select_cards(game_id=game_id[0])

    status = Status.status_check(user, dealer_value=dealer)

    if status is None:
        return jsonify({"message": "DRAW"})
    elif status is True:
        ChipsLedger().insert(current_user, bet)
        return jsonify({"message": f"Congratulations you won {bet} $"})
    else:
        ChipsLedger().insert(current_user, bet*(-1))
        return jsonify({"message": "Dealer wins"})


@app.route('/chips', methods=['GET'])
@token_required
def get_chips(current_user):
    """
        Return players total money
        This can only be done by the logged in user.
        Token required
        ---
        tags:
        - name: "wallet"
          description: ""
        produces:
        - application/json
        responses:
          default:
            description: successful operation
    """

    chips = ChipsLedger()
    total = chips.select_total_chips(current_user)
    if total is None:
        return jsonify(chips=0)
    return jsonify(chips=total)


@app.route('/chips/', methods=['POST'])
@token_required
def add_chips(current_user):

    """
        Add money to player wallet
        This can only be done by the logged in user.
        Token required
        ---
        tags:
        - name: "wallet"
          description: ""
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
        - in: body
          name: money
          description: Amount of money to add to players wallet
          required: true
          schema:
            properties:
              amount:
                type: integer
        responses:
          default:
            description: successful operation
    """
    data = request.get_json()
    if 'amount' not in data:
        return make_response('Data is missing', 400)

    if int(data['amount']) <= 0:
        return make_response('Incorrect amount', 400)

    cash = data['amount']
    chips = ChipsLedger()
    chips.insert(current_user, int(cash))
    return jsonify({"message": str(cash) + "$ added"})


@app.route('/forgot_password', methods=["POST"])
def forgot_password():
    """
    Forgot password
    Send an email to the user
    ---
      tags:
        - user
      summary: Create user
      description:
      consumes:
        - application/json
      produces:
        - application/json
      parameters:
        - in: body
          name: email
          description: Send password to user email
          required: true
          schema:
            properties:
              email:
                type: string
      responses:
        default:
          description: successful operation
    """
    data = request.get_json()

    if not data or not data["email"]:
        return jsonify({"message": "Email is missing"})

    user = User()
    check = user.select_user_by_email(data["email"])

    if check is None:
        return jsonify({"message": "Sorry, no user with such email"})
    else:
        send_email(data["email"])
        return jsonify({"message": "Please check your mail"})


@app.route('/update', methods=["PUT"])
@token_required
def update_user(current_user):
    """
        User to update
        This can only be done by the logged in user.
        Token required
        ---
          tags:
            - user
          summary: Create user
          description:
          consumes:
            - application/json
          produces:
            - application/json
          parameters:
            - in: body
              name: body
              description: Update user
              schema:
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

    if not data:
        return jsonify({"message": "Nothing to update"})

    if not all(data[i] for i in ['name', 'email', 'password']):
        return jsonify({"message": "No data to update"})

    if data["name"]:
        name = data["name"]
        user = User()
        user.update_name(current_user, name)

    if data["email"]:
        name = data["name"]
        user = User()

        if not user.select_user_by_email(data["email"]):
            user.update_name(current_user, name)
        else:
            return jsonify({"message": "User with such email"
                                       " already exist"})

    if data["password"]:
        password = bcrypt.hashpw(data['password'].encode('utf-8'),
                                 bcrypt.gensalt(10)).decode('utf-8')
        user = User()
        user.update_password(current_user, password)

    return jsonify({"message": "User successfully updated"})


if __name__ == '__main__':
    app.run(debug=True)
