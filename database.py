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

    def create(self):
        c.execute("""CREATE TABLE IF NOT EXISTS user (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,
                    email VARCHAR(100),
                    password VARCHAR(100)
                    )
                    """)

    def insert(self, name, email, password):
        c.execute("INSERT INTO user (user_name, email, password)"
                  " VALUES (?,?,?)", [name, email, password])
        conn.commit()

    def update_name(self, user_id, name):
        c.execute("UPDATE user "
                  "SET user_name = ? "
                  "WHERE user_id = ? ", [name, user_id])
        conn.commit()

    def update_email(self, user_id, email):
        c.execute("UPDATE user "
                  "SET email = ? "
                  "WHERE user_id = ?", [email, user_id])
        conn.commit()

    def update_password(self, user_id, password):
        c.execute("UPDATE user "
                  "SET password = ? "
                  "WHERE user_id = ? ", [password, user_id])
        conn.commit()

    def delete_user(self, user_id):
        c.execute("DELETE FROM user WHERE user_id=?", [user_id])
        conn.commit()

    def select_user_id(self):
        c.execute('SELECT user_id FROM user LIMIT 1')

    def select_user_id_by_email(self, email: str) -> int:
        c.execute('SELECT user_id FROM user WHERE email=?', [email])
        id = c.fetchone()
        return int(id)

    def select_user_by_email(self, email):
        c.execute('SELECT * FROM user WHERE email=?', [email])

        return c.fetchone()


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
        conn.commit()

    def select_total_chips(self, id):
        c.execute('SELECT SUM(chips) FROM chips_ledger '
                  'WHERE user_id=? GROUP BY user_id', [id])
        chips = c.fetchone()
        if chips is None:
            return None
        else:
            return chips[0]


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
        conn.commit()

    def select_game_id(self, user_id):
        c.execute('SELECT MAX(game_id) FROM game '
                  'WHERE (user_id=?)', (user_id, ))
        return c.fetchone()

    def select_bet(self, user, game):
        c.execute('SELECT bet FROM game '
                  'WHERE user_id=? AND game_id=?', [user, game])
        return c.fetchone()


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
        conn.commit()

    def select_cards(self, game_id: int) -> list[object]:
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
        conn.commit()

    def select_one_card(self, game_id: int) -> list[object]:
        c.execute('SELECT card_id FROM dealer_cards '
                  'WHERE (game_id=?) LIMIT 1', [game_id])
        card = c.fetchone()
        return [Card.from_id(card[0])]

    def select_cards(self, game_id: int) -> list[object]:
        c.execute('SELECT card_id FROM dealer_cards '
                  'WHERE (game_id=?)', [game_id])
        res = [Card.from_id(i[0]) for i in c.fetchall()]
        return res
