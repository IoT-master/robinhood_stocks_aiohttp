from Robinhood import Robinhood
from time import sleep
from pathlib import Path


class Usage(Robinhood):

    async def main(self):
        await self.login()
        watch_file = Path('Confidential/watch_list.json')
        if watch_file.exists():
            watch_list = self.load_from_json(str(watch_file))
            watch_list = set(watch_list)
        else:
            watch_list = []
            self.save_to_json(str(watch_file), watch_list)

        while True:
            self.clear_screen()
            quotes_response = await self.get_quotes(watch_list)
            quotes_response = list(filter(lambda x: x, quotes_response))
            sorted_stocks = sorted(
                quotes_response, key=lambda x: abs(float(
                    x['last_trade_price']) - float(x['previous_close']))/float(x['previous_close']),
                reverse=True)
            for each_ticker in sorted_stocks:
                last_known_price = float(each_ticker['last_trade_price'])
                bid_price = float(each_ticker['bid_price'])
                ask_price = float(each_ticker['ask_price'])
                previous_close = float(each_ticker['previous_close'])
                extended_price = float(each_ticker['last_extended_hours_trade_price']) - float(
                    each_ticker['last_trade_price']) if each_ticker['last_extended_hours_trade_price'] else 0
                print(
                    f"{each_ticker['symbol'].rjust(8, ' ')} [dP/dt: {last_known_price-previous_close:8.2f}] [last: {last_known_price:8.2f}], [bid: {bid_price:8.2f}], [ask: {ask_price:8.2f}] {extended_price:8.2f}")
            sleep(5)


if __name__ == '__main__':
    instance = Usage()
