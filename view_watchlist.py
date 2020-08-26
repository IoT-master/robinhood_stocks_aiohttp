from time import sleep

from Robinhood import Robinhood
from pathlib import Path
from colorama import init
from colorama import Fore, Back, Style


init(autoreset=True)


class Usage(Robinhood):

    async def main(self):
        await self.login()
        print('\033[2J')
        watch_file = Path('Confidential/watch_list.json')
        if watch_file.exists():
            watch_list = self.load_from_json(str(watch_file))
            watch_list = set(watch_list)
        else:
            watch_list = []
            self.save_to_json(str(watch_file), watch_list)

        while True:
            # print('\033[2J')
            # print('\033[F')
            print('\033[H')
            quotes_response = await self.get_quotes(watch_list)
            quotes_response = list(filter(lambda x: x, quotes_response))
            sorted_stocks = sorted(
                quotes_response, key=lambda x: abs(float(
                    x['last_trade_price']) - float(x['previous_close'])) / float(x['previous_close']),
                reverse=True)
            for index, each_ticker in enumerate(sorted_stocks):
                last_known_price = float(each_ticker['last_trade_price'])
                bid_price = float(each_ticker['bid_price'])
                ask_price = float(each_ticker['ask_price'])
                previous_close = float(each_ticker['previous_close'])
                extended_price = float(each_ticker['last_extended_hours_trade_price']) - float(
                    each_ticker['last_trade_price']) if each_ticker['last_extended_hours_trade_price'] else 0
                alt_background = Back.BLUE if index % 2 == 0 else Back.BLACK
                to_printout = f"{each_ticker['symbol'].rjust(8, ' ')} [dP/dt: {last_known_price - previous_close:8.2f}] [last: {last_known_price:8.2f}], [bid: {bid_price:8.2f}], [ask: {ask_price:8.2f}] "
                if not self.is_market_open():
                    to_printout += f"{extended_price:8.2f}"
                print(alt_background + (Fore.RED if last_known_price - previous_close <
                                        0 else Fore.GREEN) + to_printout)
            sleep(.5 if self.is_market_open() else 5)


if __name__ == '__main__':
    instance = Usage()
