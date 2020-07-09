from Robinhood import Robinhood


class Usage(Robinhood):

    async def main(self):
        await self.login()
        while True:
            options_dict, ticker_instrument_dict = await self.get_option_positions_from_account()
            # options_dict = self.load_from_json('senhmo4.json')
            self.clear_screen()
            options_list = []
            for each_ticker in options_dict:
                for each_option in options_dict[each_ticker]:
                    each_option['ticker'] = each_ticker
                    options_list.append(each_option)
            sorted_options = sorted(
                options_list, key=lambda x: x['dB'], reverse=True)

            stock_list = [keys for keys in ticker_instrument_dict]
            get_quotes_response = await self.get_quotes(stock_list)
            # For Option Names that were change during consolidation
            last_traded_price_dict = {}
            for each in zip(stock_list, get_quotes_response):
                if each[1]:
                    last_traded_price_dict[each[0]] = each[1]['last_trade_price']

            for stats in sorted_options:
                last_traded_price = float(last_traded_price_dict[stats['ticker']]) if stats['ticker'] in last_traded_price_dict else 0
                profit = stats['quantity'] * (stats['mark_price'] * 100 - stats['average_price'])
                print(
                    f"{stats['ticker'].rjust(8, ' ')} [last_traded_value at {last_traded_price:6.2f}], {stats['quantity']} {stats['type']} at {stats['strike_price']:6.1f} {stats['expiration_date']} [Profit: {profit:10.2f}], [db: {stats['dB']:6.2f}]")


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
