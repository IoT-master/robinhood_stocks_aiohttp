from Robinhood import Robinhood


class Usage(Robinhood):

    async def main(self):
        await self.login()
        options_dict = await self.get_option_positions_from_account()
        self.save_to_json('senhmo.json', options_dict)


if __name__ == '__main__':
    instance = Usage()

