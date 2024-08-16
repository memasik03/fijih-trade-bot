from main import tokens
import random
import time
import threading

class taptal:

    __min_price = 2
    __change_range = 500
    __t = tokens()

    def __init__(self) -> None:
        try:
            self.__t.create_token("TAPTAL", 50000, 1000000)
        except:
            pass

    def update_price(self):
        while True:
            change_range_round = int(round(self.__change_range / 10))
            summ = random.randint(-change_range_round * 10, change_range_round * 10)
            if summ >= 0 and self.__t.get_token_price("TAPTAL") + summ > self.__min_price:
                self.__t.buy_token("TAPTAL", abs(summ))
            else:
                self.__t.sell_token("TAPTAL", abs(summ))
            print(self.__t.get_token_price("TAPTAL", True))
            time.sleep(5)
    
    def start(self):
        taptal_price_thread = threading.Thread(target=self.update_price)
        taptal_price_thread.start()