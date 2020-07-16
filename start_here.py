from Robinhood import Robinhood
from pprint import pprint


class Usage(Robinhood):

    async def main(self):
        await self.login()
        options_dict = await self.get_option_positions_from_account()
        pprint(options_dict)


if __name__ == '__main__':
    instance = Usage()
