from Robinhood import Robinhood
from time import sleep


class Usage(Robinhood):

    async def main(self):
        await self.login()
        while True:
            options_dict = await self.get_option_positions_from_account()
            # options_dict = self.load_from_json('senhmo4.json')
            self.clear_screen()
            options_list = []
            for each_ticker in options_dict:
                for each_option in options_dict[each_ticker]:
                    each_option['ticker'] = each_ticker
                    options_list.append(each_option)
            sorted_options = sorted(
                options_list, key=lambda x: x['dB'], reverse=True)

            for stats in sorted_options:
                print(
                    f"{stats['ticker'].rjust(8, ' ')} {stats['quantity']} Strike {stats['type']}: {stats['strike_price']:10.1f} Profit: {stats['quantity']*(stats['mark_price']*100-stats['average_price']):10.2f} EXP: {stats['expiration_date']} {stats['type']} {stats['dB']:.2f}")


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
