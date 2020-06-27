from Robinhood import Robinhood


class Usage(Robinhood):
    async def main(self):
        await self.login()
        # data = await self.get_quotes(['tsla','amd'])
        data = await self.get_stock_historicals(['amd', 'tsla'])
        self.save_to_json_dict('senhmo.json', data)


if __name__ == '__main__':
    instance = Usage()
