import telebot
from telebot import types
from main import *
from users import users
from jokes.fijih_taptal import taptal
import re

bot = telebot.TeleBot("ne")

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
    try:
        wallet = w.get_address(message.from_user.username)
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
    except:
        bot.send_message(message.chat.id, f"Ошибка")



@bot.message_handler(commands=["sell"])
def enter_count(message):
    u.start(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Введите количество для продажи:")
    bot.register_next_step_handler(message, sell)

def sell(message):
    try:
        wallet = w.get_address(message.from_user.username)
        sell_summ = t.get_token_price("TAPTAL", True) * float(message.text)

        if float(message.text) < t.min_purchase_price:
            bot.send_message(message.chat.id, f"Минимальная цена покупки/продажи - {t.min_purchase_price}$")
            return
        elif float(message.text) > h.get_token_count("TAPTAL", wallet):
            bot.send_message(message.chat.id, f"Недостаточно токенов на кошельке")
        else:
            w.change_balance(wallet, -sell_summ)
            t.sell_token("TAPTAL", float(message.text))
            h.add_holder("TAPTAL", -float(message.text), wallet)
            bot.send_message(message.chat.id, f"Вы успешно продали <b>{float(message.text)} TAPTAL</b> за <b>{sell_summ}$</b>", parse_mode="html")
    except:
        bot.send_message(message.chat.id, f"Ошибка")



@bot.message_handler(commands=["course"])
def course(message):
    bot.send_message(message.chat.id, f"<b>{t.get_token_price("TAPTAL", True)}$</b>", parse_mode="html")



@bot.message_handler(commands=["wallets"])
def wallets_list(message):
    u.start(message.chat.id, message.from_user.username)
    user_address = w.get_address(message.from_user.username)
    wallets_markup = types.InlineKeyboardMarkup()
    user_wallets = w.get_wallet(user_address)
    if len(user_wallets) == 1:
        result = f"🔤 <b>Адрес кошелька</b>: {user_wallets[0][1]}\n🏷️ <b>Имя кошелька</b>: {u.get_wallet_name(w.get_wallet(user_address)[0][1])}\n💵 <b>USD</b>: {w.get_balance(user_address)}\n<b>Токены</b>:\n"
        for token in h.get_holder_info(user_address):
            token_count = token[2]
            token_name = token[1]
            if token == h.get_holder_info(user_address)[-1]:
                result += f"╚ {token_count} <b>{token_name}</b> <i>({round(t.get_token_price(token_name, True) * token_count, 3)}$)</i>"
            else:
                result += f"╠ {token_count} <b>{token_name}</b> <i>({round(t.get_token_price(token_name, True) * token_count, 3)}$)</i>"
        bot.send_message(message.chat.id, result, parse_mode="html")
    else:
        for i in range(user_wallets):
            wallets_markup.add(types.InlineKeyboardButton(f"{u.get_wallet_name(i[1])}", callback_data="anal"))
            bot.send_message(message.chat.id, "Выебите кошелек:", reply_markup=wallets_markup)

def isdigit(num):
    match = re.search(r"\.\d+", str(num))
    return match

bot.polling()