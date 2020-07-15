from Robinhood import Robinhood
from time import sleep

class Usage(Robinhood):

    async def main(self):
        await self.login()
        watch_list = ['LYV', 'TSLA', 'MRNA', 'NIO', 'BA', 'NVDA']
        while True:
            self.clear_screen()
            quotes_response = await self.get_quotes(watch_list)
            # self.save_to_json('senhmo.json', quotes_response)
            for each_ticker in quotes_response:
                last_known_price = float(each_ticker['last_extended_hours_trade_price'] if 'last_extended_hours_trade_price' in each_ticker else each_ticker['last_extended_hours_trade_price'])
                bid_price = float(each_ticker['bid_price'])
                ask_price = float(each_ticker['ask_price'])
                previous_close = float(each_ticker['previous_close'])
                print(f"{each_ticker['symbol'].rjust(8, ' ')} [dP/dt: {last_known_price-previous_close:8.2f}] [last: {last_known_price:8.2f}], [bid: {bid_price:8.2f}], [ask: {ask_price:8.2f}]")
            sleep(.5)


if __name__ == '__main__':
    instance = Usage()