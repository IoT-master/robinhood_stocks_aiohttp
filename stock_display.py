from Robinhood import Robinhood
from time import sleep


class Usage(Robinhood):

    async def main(self):
        await self.login()
        while True:
            stocks = await self.get_stock_positions_from_account()
            self.clear_screen()
            sorted_stocks = sorted(
                stocks.items(), key=lambda x: x[1]['status']['dB'], reverse=True)
            for k, v in sorted_stocks:
                stats = v['status']
                print(
                    f"{k.rjust(8, ' ')}: [abp {float(v['average_buy_price']):10.2f}], [last {stats['last']:9.2f}], [bid: {stats['bid']:10.2f}], [ask: {stats['ask']:10.2f}], [real_last:{stats['extended']:10.2f}], [%: {stats['percent']:6.2f}], [dB:{stats['dB']:6.3f}]")
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
