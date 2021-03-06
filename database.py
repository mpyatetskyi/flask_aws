import sqlite3
from methods import Card

conn = sqlite3.connect('blackjack.db', check_same_thread=False)
c = conn.cursor()


class DatabaseTables:

    def drop(self, table_name):
        c.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    def truncate(self, table_name):
        c.execute(f'DELETE FROM "{table_name}" ')
        c.execute('VACUUM')
        return f"{table_name} is truncated"


class User(DatabaseTables):

    def __init__(self):
        pass

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS user (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT
                    )
                    """)

    def insert(self, name):
        c.execute("INSERT INTO user (user_name)"
                  " VALUES (?)", [name])
        return 'Success'

    def select_user_id(self):
        c.execute('SELECT user_id FROM user LIMIT 1')

        return c.fetchall()


class ChipsLedger(DatabaseTables):

    def __init__(self):
        pass

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS chips_ledger (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    chips INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(user_id)
                    )""")

    def insert(self, user, chips):
        c.execute("INSERT INTO chips_ledger (user_id, chips)"
                  " VALUES (?,?)", [user, chips])

    def select_total_chips(self, id):
        c.execute('SELECT SUM(chips) FROM chips_ledger '
                  'WHERE user_id=? GROUP BY user_id', [id])
        return c.fetchone()


class Game(DatabaseTables):

    def __init__(self):
        pass

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS game (
                    game_id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    bet INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user(user_id)
                    )""")

    def insert(self, user_id, bet):
        c.execute('INSERT INTO game (user_id, bet)'
                  'VALUES (?,?)', [user_id, bet])

    def select_game_id(self, user_id):
        c.execute('SELECT MAX(game_id) FROM game '
                  'WHERE (user_id=?)', (user_id, ))
        return c.fetchone()

    def select_bet(self, id):
        c.execute('SELECT bet FROM game '
                  'WHERE user_id=?', [id])
        return


class UserCards(DatabaseTables):

    def __init__(self):
        pass

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS user_cards(
                    game_id INTEGER NOT NULL,
                    card_id INTEGER NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES game(game_id),
                    PRIMARY KEY (game_id, card_id)
                    )""")

    def insert(self, game_id, card_id):
        c.execute('INSERT INTO user_cards (game_id, card_id)'
                  'VALUES (?,?)', [game_id, card_id])

    def select_cards(self, game_id):
        c.execute('SELECT card_id FROM user_cards '
                  'WHERE (game_id=?)', [game_id])
        return [Card.from_id(i[0]) for i in c.fetchall()]


class DealerCards(DatabaseTables):

    def __init__(self):
        pass

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS dealer_cards(
                    game_id INTEGER NOT NULL,
                    card_id INTEGER NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES game(game_id),
                    PRIMARY KEY (game_id, card_id)
                    )""")

    def insert(self, game_id, card_id):
        c.execute('INSERT INTO dealer_cards (game_id, card_id)'
                  'VALUES (?,?)', [game_id, card_id])

    def select_one_card(self, game_id):
        c.execute('SELECT card_id FROM dealer_cards '
                  'WHERE (game_id=?) LIMIT 1', [game_id])
        card = c.fetchone()
        return [Card.from_id(card[0])]

    def select_cards(self, game_id):
        c.execute('SELECT card_id FROM dealer_cards '
                  'WHERE (game_id=?)', [game_id])
        res = [Card.from_id(i[0]) for i in c.fetchall()]
        return res
