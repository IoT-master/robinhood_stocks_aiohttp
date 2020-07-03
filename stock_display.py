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
                    f"{k.rjust(8, ' ')}: bid: {stats['bid']:10.2f}, ask: {stats['ask']:10.2f}, last {stats['last']:9.2f}, real_last:{stats['extended']:10.2f}, %: {stats['percent']:6.2f}, dB:{stats['dB']:6.3f}")
            sleep(2)


if __name__ == '__main__':
    instance = Usage()
