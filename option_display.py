from time import sleep

from Robinhood import Robinhood


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
                    last_traded_price_dict[each[0]] = float(each[1]['last_trade_price'])
                    previous_closed_price_dict[each[0]] = float(each[1]['adjusted_previous_close'])

            options_list = []
            for each_ticker in options_dict:
                for each_option in options_dict[each_ticker]:
                    each_option['ticker'] = each_ticker
                    if each_ticker in last_traded_price_dict:
                        each_option['last_trade_price'] = last_traded_price_dict[each_ticker]
                        each_option['price_change'] = last_traded_price_dict[each_ticker] - previous_closed_price_dict[each_ticker]
                    else:
                        each_option['price_change'] = 0
                    options_list.append(each_option)

            # Sort Functionality
            sorted_options = sorted(
                options_list, key=lambda x: x['price_change'], reverse=True)

            total_from_profits = 0
            total_daily_profit = 0
            for stats in sorted_options:
                last_traded_price = last_traded_price_dict[stats['ticker']] if stats[
                                                                                   'ticker'] in last_traded_price_dict else 0
                profit = stats['quantity'] * (stats['mark_price'] * 100 - stats['average_price'])
                position = 'buy ' if stats['quantity'] > 0 else 'sell'
                daily_profit_per_option = (stats['mark_price'] - float(stats['previous_close_price'])) * 100
                total_from_profits += profit
                total_daily_profit += daily_profit_per_option
                print(
                    f"{stats['ticker'].rjust(5, ' ')} {stats['price_change']:5.2f} [Daily_Profit: {daily_profit_per_option:7.2f}] [TotProfit: {profit:8.2f}] [s at {last_traded_price:6.2f}] [v at {float(stats['adjusted_mark_price']):7.2f}] {stats['quantity']} {position} {stats['type']} at {stats['strike_price']:5.1f} {stats['expiration_date']} [delta: {stats['delta']}] [gamma: {stats['gamma']}] [iv: {stats['implied_volatility']}] [theta: {stats['theta']}] [rho: {stats['rho']}] [vega: {stats['vega']}]")
            print(
                "\033[36m" + f"Total Profits: {total_from_profits:10.2f} Daily Profits: {total_daily_profit:.2f}" + "\033[0m")
            sleep(.5)


if __name__ == '__main__':
    instance = Usage()
    test = {
        'DIA': [{'2020-06-26T16:00:00Z': '251.960000'}, [265], ['BC', .35, '7/17/2020'],
                {'2020-06-26T19:00:00Z': '250.500000'}],
        'SMH': [{'2020-06-26T16:00:00Z': '148.890000'}, [135], ['SP', .27, '7/17/2020'],
                {'2020-06-26T19:00:00Z': '148.070000'}],
        'TLT': [{'2020-06-24T16:00:00Z': '165.010000'}, [170], ['SC', .17, '7/17/2020'],
                {'2020-06-26T19:00:00Z': '165.250000'}],
        'GLD': [{'2020-06-24T16:00:00Z': '166.040000'}, [160], ['BP', .28, '7/17/2020'],
                {'2020-06-26T19:00:00Z': '165.250000'}],
    }
