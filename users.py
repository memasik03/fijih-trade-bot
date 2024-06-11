import sqlite3
from main import wallets

def toDB(command, tuple="", fetch=False):
    connection = sqlite3.connect("users.sql")
    cursor = connection.cursor()
    result = ()
    if fetch:
        result = cursor.execute(command, tuple).fetchall()
    else:
        cursor.execute(command, tuple)
        connection.commit()
    cursor.close()
    connection.close()
    return result

class users:
    max_wallets = 5
    __default_wallet_name = "main"

    def __init__(self) -> None:
        toDB("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, tg_username TEXT)")
        toDB("CREATE TABLE IF NOT EXISTS wallets (id INTEGER PRIMARY KEY AUTOINCREMENT, tg_username TEXT, wallet_address TEXT, wallet_name TEXT)")

    def start(self, tg_id, tg_username):
        user = toDB("SELECT * FROM users WHERE tg_id = (?) AND tg_username = (?)", (tg_id, tg_username), True)
        if user == []:
            toDB("INSERT INTO users (tg_id, tg_username) VALUES (?, ?)", (tg_id, tg_username))
            wallet = wallets()
            wallet.create_wallet(tg_username)
            toDB("INSERT INTO wallets (tg_username, wallet_address, wallet_name) VALUES (?, ?, ?)", (tg_username, wallet.get_wallet(tg_username), self.__default_wallet_name))
        else:
            return user[0]