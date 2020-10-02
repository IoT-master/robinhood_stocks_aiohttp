from time import sleep
from dateutil.parser import parse
from Robinhood import Robinhood
from datetime import datetime, timedelta
from colorama import init
from colorama import Fore, Back, Style
from dateutil.tz import gettz
import re


init(autoreset=True)


class Usage(Robinhood):

    async def main(self):
        await self.login()
        print('\033[2J')
        num_of_options = 0
        while True:
            options_dict, ticker_instrument_dict = await self.get_option_positions_from_account()
            # print('\033[2J')
            # print('\033[F')
            print('\033[H')
            # Extracting the Tickers Names from the Options
            stock_list = [ticker for ticker in ticker_instrument_dict]
            screened_stock_list = list(map(
                lambda x: re.search(r"[A-Z]+", x).group(), stock_list))
            # screened_stock_list = filter(
            #     lambda x: x != 'HYLN', screened_stock_list)
            get_quotes_response = await self.get_quotes(screened_stock_list)

            previous_closed_price_dict = {}
            last_traded_price_dict = {}
            after_market_change_dict = {}
            # Getting Stock Info of the Option
            for each in zip(stock_list, get_quotes_response):
                last_traded_price_dict[each[0]] = float(each[1]['last_extended_hours_trade_price']) if each[1][
                    'last_extended_hours_trade_price'] else float(each[1]['last_trade_price'])
                previous_closed_price_dict[each[0]] = float(
                    each[1]['adjusted_previous_close'])
                after_market_change_dict[each[0]] = (float(each[1]['last_extended_hours_trade_price']) - float(each[1]['last_trade_price'])) if each[1][
                    'last_extended_hours_trade_price'] else 0

            options_list = []
            for each_ticker in options_dict:
                for each_option in options_dict[each_ticker]:
                    each_option['ticker'] = each_ticker
                    if each_ticker in last_traded_price_dict:
                        each_option['last_trade_price'] = last_traded_price_dict[each_ticker]
                        each_option['price_change'] = last_traded_price_dict[each_ticker] - previous_closed_price_dict[
                            each_ticker]
                    else:
                        each_option['price_change'] = 0
                    options_list.append(each_option)

            # Sort Functionality
            sorted_options = sorted(
                options_list, key=lambda x: x['price_change'], reverse=True)
            # options_list, key=lambda x: x['quantity'] * (float(x['adjusted_mark_price']) * 100 - x['average_price']), reverse=True)

            total_from_profits = 0
            total_daily_profit = 0
            total_value = 0
            total_print = []
            num_of_new_options = len(sorted_options)
            if num_of_new_options != num_of_options:
                print('\033[2J')
                print('\033[H')
                num_of_options = num_of_new_options
            for index, stats in enumerate(sorted_options):
                right_now = datetime.now(tz=gettz('America/New_York'))
                same_day = datetime(right_now.year, right_now.month, right_now.day, 9, 30, 0,
                                    tzinfo=gettz('America/New_York')) - parse(stats['created_at']) < timedelta(days=1)
                last_traded_price = last_traded_price_dict[stats['ticker']] if stats[
                    'ticker'] in last_traded_price_dict else 0

                position = 'buy ' if stats['average_price'] > 0 else 'sell'
                close_position = 1 if stats['average_price'] > 0 else -1
                daily_profit_per_option = stats['quantity'] * (float(
                    stats['adjusted_mark_price'])*100 - float(stats['previous_close_price'])*100)
                aftermarket_price_change = after_market_change_dict.get(
                    stats['ticker'], 0)
                # TODO: Fix this logic when I can get the datetime of an option after duplicating an option
                # Only way to tell when you are buying vs selling option(s)
                if stats['average_price'] > 0:
                    profit = stats['quantity'] * \
                        (float(stats['mark_price'])
                         * 100 - stats['average_price'])
                    true_daily_profit = profit if same_day else daily_profit_per_option
                else:
                    profit = stats['quantity'] * \
                        (-float(stats['mark_price'])
                         * 100 + -stats['average_price'])
                    true_daily_profit = profit if same_day else stats['quantity'] * (-float(
                        stats['adjusted_mark_price'])*100 + float(stats['previous_close_price'])*100)
                total_from_profits += profit
                total_daily_profit += true_daily_profit
                adjusted_adjusted_mark_price = float(
                    stats['adjusted_mark_price']) * 100 if position == 'buy ' else -float(stats['adjusted_mark_price']) * 100
                total_value += stats['quantity'] * adjusted_adjusted_mark_price
                alt_background = Back.BLUE if index % 2 == 0 else Back.BLACK
                color_warning = Fore.YELLOW if abs(float(
                    stats['mark_price'])*100 - stats['average_price'])/stats['average_price'] < .1 else ""
                to_printout = alt_background + color_warning + \
                    f"{stats['ticker'].rjust(5, ' ')} " + Fore.RESET
                for each in ['delta', 'gamma', 'rho', 'theta', 'vega', 'implied_volatility']:
                    stats[each] = 0.0 if stats[each] == None else float(
                        stats[each])
                time_before_expiration = parse(
                    stats['sellout_datetime']) - datetime.now(tz=gettz('America/New_York'))
                option_quantity = int(stats['quantity'])
                if not self.is_market_open():
                    to_printout += f"{aftermarket_price_change: 6.2f} [${option_quantity*close_position*aftermarket_price_change*stats['delta']*100: 8.2f}] "
                to_printout += f"{stats['price_change']:6.2f} [DP:${true_daily_profit:8.2f}] "
                to_printout += (Fore.RED if profit <
                                0 else Fore.GREEN) + f" [TP:${profit:8.2f}] " + "\033[0m" + alt_background + f"[s: {last_traded_price:7.2f}] [v: {float(stats['adjusted_mark_price']):7.2f}] {option_quantity:2} {position} {stats['type'].rjust(4, ' ')}  [k: {stats['strike_price']:5.1f}] {stats['expiration_date']} [delta: {stats['delta']:5.2f}] [gamma: {stats['gamma']:4.2f}] [iv: {stats['implied_volatility']:4.2f}] [theta: {stats['theta']:5.2f}] [rho: {stats['rho']:5.2f}] [vega: {stats['vega']:5.2f}] [{time_before_expiration.days:3} day(s)] "
                to_printout += f"{float(stats['average_price'])/100:7.2f} "
                # to_printout += f"{last_traded_price - stats['strike_price']:7.2f}"
                to_printout += Back.RESET

                total_print.append(to_printout + Back.RESET)
            print('\n'.join(total_print) + '\n' +
                  f"[Total Value: {total_value:10.2f}] [Total Profits: {total_from_profits:10.2f}] [Daily Profits: {total_daily_profit:.2f}]")
            sleep(.5 if self.is_market_open() else 5)


if __name__ == '__main__':
    instance = Usage()
