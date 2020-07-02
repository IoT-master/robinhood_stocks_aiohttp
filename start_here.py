from Robinhood import Robinhood

class Usage(Robinhood):

    @staticmethod
    def filtering_options_body(each_option_owned, option_details):
        return {
            'type': each_option_owned['type'],
            'quantity': each_option_owned['quantity'],
            'created_at': each_option_owned['created_at'],
            'average_price': each_option_owned['average_price'],
            'option_id': each_option_owned['option_id'],
            'adjusted_mark_price': option_details['adjusted_mark_price'],
            'ask_price': option_details['ask_price'],
            'ask_size': option_details['ask_size'],
            'bid_price': option_details['bid_price'],
            'bid_size': option_details['bid_size'],
            'mark_price': option_details['mark_price'],
            'previous_close_price': option_details['previous_close_price'],
            'chance_of_profit_long': option_details['chance_of_profit_long'],
            'chance_of_profit_short': option_details['chance_of_profit_short'],
            'delta': option_details['delta'],
            'gamma': option_details['gamma'],
            'implied_volatility': option_details['implied_volatility'],
            'rho': option_details['rho'],
            'theta': option_details['theta'],
            'vega': option_details['vega'],
            'greek': option_details
                }

    async def main(self):
        await self.login()
        # data = await self.get_stock_positions_from_account()
        data = await self.get_open_option_positions()
        options_dict = {}
        for each_option in data[0]:
            greeks_dict = await self.get_option_market_data_by_id(each_option['option_id'])
            ticker_symbol = each_option['chain_symbol']
            if ticker_symbol not in options_dict:
                options_dict[ticker_symbol] = [Usage.filtering_options_body(each_option, greeks_dict)]
            else:
                options_dict[ticker_symbol].append(Usage.filtering_options_body(each_option, greeks_dict))
        self.save_to_json('senhmo.json', options_dict)
        self.save_to_json('senhmo2.json', data)



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
