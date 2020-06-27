from pprint import pprint

import ujson

from Robinhood import Robinhood


class Usage(Robinhood):
    async def main(self):
        await self.login()
        # data = await self.get_quotes(['tsla','amd'])
        # data = await self.get_stock_historicals(['WKHS', 'DIA', 'TLT', 'SMH'])
        # self.save_to_json_dict('senhmo.json', data)
        with open('senhmo.json', 'r') as f:
            data = ujson.loads(f.read())
        stock_diff = {}
        for each_stock_section in data:
            for each_ticker in each_stock_section:
                open_price_list = []
                stock_name = each_ticker
                for each_item in each_stock_section[each_ticker]:
                    for each2 in each_item:
                        open_price_list.append({each2['begins_at']: each2['open_price']})
                stock_diff[stock_name] = open_price_list

        pprint(stock_diff)


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
