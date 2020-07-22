from Robinhood import Robinhood
from time import sleep
from colorama import init
from colorama import Fore, Back, Style
from tabulate import tabulate


init()


class Usage(Robinhood):

    async def main(self):
        await self.login()
        while True:
            stocks = await self.get_stock_positions_from_account()
            self.clear_screen()
            sorted_stocks = sorted(
                stocks.items(), key=lambda x: x[1]['status']['extended'] - float(x[1]['average_buy_price']), reverse=True)
            total_profit = 0
            total_daily_profit = 0
            total_value = 0
            for index, (k, v) in enumerate(sorted_stocks):
                stats = v['status']
                average_buy_price = float(v['average_buy_price'])
                profit_per_share = stats.get(
                    'extended', stats['last']) - average_buy_price
                total_value += float(v['quantity']) * stats['extended']
                total_profit += average_buy_price * float(v['quantity'])
                total_daily_profit += float(v['quantity']) * (
                    stats['extended'] - stats['adjusted_previous_close'])
                aftermarket_price_change = (
                    stats.get('extended', stats['last']) - stats['last'])
                alt_background = Back.BLUE if index % 2 == 0 else Back.BLACK
                to_printout = f"{k.rjust(8, ' ')}: [pps: {profit_per_share:6.2f}] [abp: {average_buy_price:8.2f}], [#: {float(v['quantity']):7.2f}] [last: {stats['last']:8.2f}], [bid: {stats['bid']:8.2f}], [ask: {stats['ask']:8.2f}], [real_last: {stats['extended']:8.2f}], [%: {stats['percent']:6.2f}], [dB: {stats['dB']:6.3f}]"
                if not self.is_market_open():
                    to_printout += f"{aftermarket_price_change: 6.2f}"
                print(alt_background + (Fore.RED if profit_per_share <
                                        0 else Fore.GREEN) + to_printout + Fore.RESET + Back.RESET)
            print(
                f"[Total Value {total_value:10.2f}] [Total Profits:{total_profit:10.2f}] [Daily Profits: {total_daily_profit:.2f}]" + "\033[0m")
            sleep(.5 if self.is_market_open() else 5)


if __name__ == '__main__':
    instance = Usage()