import telebot
from main import *
from users import users
from jokes.fijih_taptal import taptal

bot = telebot.TeleBot("this is not my token")

u = users()
t = tokens()
h = holders()
w = wallets()

tl = taptal()

tl.start()

@bot.message_handler(commands=["start"])
def start(message):
    u.start(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Huy")



@bot.message_handler(commands=["buy"])
def enter_count(message):
    u.start(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Введите количество для покупки:")
    bot.register_next_step_handler(message, buy)

def buy(message):
    wallet = w.get_wallet(message.from_user.username)
    purchase_summ = t.get_token_price("TAPTAL", True) * float(message.text)

    if float(message.text) < t.min_purchase_price:
        bot.send_message(message.chat.id, f"Минимальная цена покупки/продажи - {t.min_purchase_price}$")
        return
    elif w.get_balance(wallet) < t.get_token_price("TAPTAL") * float(message.text):
        bot.send_message(message.chat.id, f"Недостаточно средств")
    else:
        w.change_balance(wallet, purchase_summ)
        t.buy_token("TAPTAL", float(message.text))
        h.add_holder("TAPTAL", float(message.text), wallet)
        bot.send_message(message.chat.id, f"Вы успешно купили <b>{float(message.text)} TAPTAL</b> за <b>{purchase_summ}$</b>", parse_mode="html")



@bot.message_handler(commands=["sell"])
def enter_count(message):
    u.start(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Введите количество для продажи:")
    bot.register_next_step_handler(message, sell)

def sell(message):
    wallet = w.get_wallet(message.from_user.username)
    sell_summ = t.get_token_price("TAPTAL", True) * float(message.text)

    if float(message.text) < t.min_purchase_price:
        bot.send_message(message.chat.id, f"Минимальная цена покупки/продажи - {t.min_purchase_price}$")
        return
    elif float(message.text) < h.get_token_count("TAPTAL", wallet):
        bot.send_message(message.chat.id, f"Недостаточно токенов на кошельке")
    else:
        w.change_balance(wallet, sell_summ)
        t.sell_token("TAPTAL", float(message.text))
        h.add_holder("TAPTAL", float(message.text), wallet)
        bot.send_message(message.chat.id, f"Вы успешно продали <b>{float(message.text)} TAPTAL</b> за <b>{sell_summ}$</b>", parse_mode="html")

bot.polling()
