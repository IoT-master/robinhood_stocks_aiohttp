from Robinhood import Robinhood
import pandas as pd


class Usage(Robinhood):

    async def main(self):
        await self.login()
        options_dict = await self.find_tradable_options2('AMD')
        df = pd.DataFrame(options_dict)
        print(df.columns)
        expiration_dates = df['expiration_date']
        strike_prices = df['strike_price']
        print(sorted(expiration_dates.unique()))
        print(sorted(strike_prices.unique()))


if __name__ == '__main__':
    instance = Usage()
