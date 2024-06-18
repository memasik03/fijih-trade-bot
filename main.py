import sqlite3
import hashlib

def toDB(command, tuple="", fetch=False):
    connection = sqlite3.connect("wallets.sql")
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



class wallets:
    __start_balance = 300.0

    def __init__(self) -> None:
        toDB("""CREATE TABLE IF NOT EXISTS wallets (
            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            holder_name TEXT,
            usd FLOAT
            
            )""")
    def get_address(self, holder_name):
        result = toDB("SELECT * FROM wallets WHERE holder_name = (?)", (holder_name,), True)
        if result == []:
            raise ValueError("Wallet not found")
        else:
            return result[0][1]

    def get_balance(self, wallet_address):
        result = toDB("SELECT * FROM wallets WHERE address = (?)", (wallet_address,), True)
        if result == []:
            raise ValueError("Wallet not found")
        else:
            return result[0][3]

    def get_wallet(self, wallet_address):
        result = toDB("SELECT * FROM wallets WHERE address = (?)", (wallet_address,), True)
        if result == []:
            raise ValueError("Wallet not found")
        else:
            return result

    def create_wallet(self, holder_name):
        hash_object = hashlib.sha256(str(len(toDB("SELECT * FROM wallets", (), True))).encode())
        wallet_address = hash_object.hexdigest()
        print(wallet_address)
        toDB("INSERT INTO wallets (address, holder_name, usd) VALUES (?, ?, ?)", (wallet_address, holder_name, self.__start_balance))

    def change_balance(self, wallet_address, change_a_lot):
        toDB("UPDATE wallets SET usd = usd - (?) WHERE address = (?)", (change_a_lot, wallet_address))



class holders:
    def __init__(self) -> None:
        toDB("""CREATE TABLE IF NOT EXISTS holders (
            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_name TEXT,
            token_count FLOAT,
            holder TEXT
            
            )""")

    def add_holder(self, token_name, token_count, holder_address):
        if toDB("SELECT * FROM holders WHERE token_name = (?) AND holder = (?)", (token_name, holder_address), True) == []:
            toDB("INSERT INTO holders (token_name, token_count, holder) VALUES (?, ?, ?)", (token_name, token_count, holder_address))
        else:
            toDB("UPDATE holders SET token_count = token_count + (?) WHERE token_name = (?) AND holder = (?)", (token_count, token_name, holder_address))

    def get_token_count(self, token_name, holder_address):
        try:
            return toDB("SELECT * FROM holders WHERE token_name = (?) AND holder = (?)", (token_name, holder_address), True)[0][2]
        except:
            return []
        
    def get_holder_info(self, holder_address):
        try:
            return toDB("SELECT * FROM holders WHERE holder = (?)", (holder_address,), True)
        except:
            return []



class tokens:
    min_purchase_price = 0.001
    max_token_name_length = 15
    __price_multiply = 10
    __price_decimal = 5

    def __init__(self) -> None:
        toDB("""CREATE TABLE IF NOT EXISTS tokens (
            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_name TEXT,
            count INTEGER,
            volume FLOAT
            
            )""")

    def create_token(self, name, count, volume):
        if toDB("SELECT * FROM tokens WHERE token_name = (?)", (name,), True) != []:
            raise ValueError(f"Token is already exist")
        elif len(name) > self.max_token_name_length:
            raise ValueError(f"Max token name length is {self.max_token_name_length}")
        else:
            toDB("INSERT INTO tokens (token_name, count, volume) VALUES (?, ?, ?)", (str(name).upper(), count, volume))

    def get_token_price(self, token_name, is_round=False):
        result = float(toDB("SELECT * FROM tokens WHERE token_name = (?)", (str(token_name).upper(),), True)[0][3] / toDB("SELECT * FROM tokens WHERE token_name = (?)", (str(token_name).upper(),), True)[0][2])
        if is_round:
            return round(result, self.__price_decimal)
        else:
            return result

    def buy_token(self, token_name, count):
        toDB("UPDATE tokens SET volume = volume + (?) WHERE token_name = (?)", (self.get_token_price(token_name) * count * self.__price_multiply, token_name))

    def sell_token(self, token_name, count):
        toDB("UPDATE tokens SET volume = volume - (?) WHERE token_name = (?)", (self.get_token_price(token_name) * count * self.__price_multiply, token_name))