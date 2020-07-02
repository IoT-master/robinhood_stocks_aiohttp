from Robinhood import Robinhood

class Usage(Robinhood):

    async def main(self):
        await self.login()
        # data = await self.get_watchlist_by_name()
        # stock_ticker_list = await self.get_list_of_instruments(data)
        # self.save_to_json('senhmo.json', stock_ticker_list)
        stock_ticker_list = self.load_from_json('senhmo.json')
        await self.display_current_status_of_stock_list_once(stock_ticker_list)



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
