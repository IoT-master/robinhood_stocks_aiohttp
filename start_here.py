from pprint import pprint


from Robinhood import Robinhood
from Robinhood.custom import open_option_positions_filter

class Usage(Robinhood):
    async def main(self):
        await self.login()
        data = await self.get_open_option_positions()
        # data = await self.get_open_option_positions(info='chain_symbol')
        # data = await self.get_quotes(['tsla','amd'])
        self.save_to_json_dict('senhmo.json', data)
        data2 = open_option_positions_filter(data)
        self.save_to_json_dict('senhmo2.json', data2)



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
