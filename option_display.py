from time import sleep
from dateutil.parser import parse
from dateutil.tz import tzlocal
from Robinhood import Robinhood
from datetime import datetime, timedelta


class Usage(Robinhood):

    async def main(self):
        await self.login()
        while True:
            options_dict, ticker_instrument_dict = await self.get_option_positions_from_account()
            self.clear_screen()
            # Extracting the Tickers Names from the Options
            stock_list = [ticker for ticker in ticker_instrument_dict]
            get_quotes_response = await self.get_quotes(stock_list)

            previous_closed_price_dict = {}
            last_traded_price_dict = {}
            # Getting Stock Info of the Option
            for each in zip(stock_list, get_quotes_response):
                # For Option Names that are NOT Stock Ticker Symbols anymore
                if each[1]:
                    last_traded_price_dict[each[0]] = float(each[1]['last_extended_hours_trade_price']) if each[1][
                        'last_extended_hours_trade_price'] else float(each[1]['last_trade_price'])
                    previous_closed_price_dict[each[0]] = float(
                        each[1]['adjusted_previous_close'])

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
            for stats in sorted_options:
                now = datetime.now()
                # same_day = parse(stats['created_at']).date() == datetime.today().date()
                same_day = datetime(now.year, now.month, now.day + 1, 8, 30, 0,
                                    tzinfo=tzlocal()) - parse(stats['created_at']) < timedelta(days=1, hours=1)
                last_traded_price = last_traded_price_dict[stats['ticker']] if stats[
                    'ticker'] in last_traded_price_dict else 0
                profit = stats['quantity'] * \
                    (float(stats['adjusted_mark_price'])
                     * 100 - stats['average_price'])
                position = 'buy ' if stats['quantity'] > 0 else 'sell'
                daily_profit_per_option = stats['quantity'] * (float(
                    stats['adjusted_mark_price'])*100 - float(stats['previous_close_price'])*100)
                aftermarket_price_change = stats['aftermarket_price_change'] if 'aftermarket_price_change' in stats else 0
                true_daily_profit = profit if same_day else daily_profit_per_option
                total_from_profits += profit
                total_daily_profit += true_daily_profit
                total_value += stats['quantity'] * \
                    float(stats['adjusted_mark_price']) * 100
                print(
                    f"{stats['ticker'].rjust(5, ' ')} {aftermarket_price_change:5.2f} {stats['price_change']:5.2f} [DP: {true_daily_profit:7.2f}] [TP: {profit:8.2f}] [s at {last_traded_price:6.2f}] [v at {float(stats['adjusted_mark_price']):7.2f}] {int(stats['quantity']):2} {position} {stats['type']} at {stats['strike_price']:5.1f} {stats['expiration_date']} [del: {stats['delta']}] [gam: {stats['gamma']}] [iv: {stats['implied_volatility']}] [the: {stats['theta']}] [rho: {stats['rho']}] [veg: {stats['vega']}]")
            print(
                "\033[36m" + f"[Total Value: {total_value:10.2f}] [Daily Profits: {total_daily_profit:.2f}] [Total Profits: {total_from_profits:10.2f}]" + "\033[0m")
            sleep(.5)


if __name__ == '__main__':
    instance = Usage()
