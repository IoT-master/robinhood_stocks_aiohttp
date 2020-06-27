from pprint import pprint

from Robinhood import Robinhood


class Usage(Robinhood):
    async def main(self):
        await self.login()
        # data = await self.get_quotes(['tsla','amd'])
        data = await self.get_stock_historicals(['WKHS', 'DIA', 'TLT', 'SMH'])
        self.save_to_json_dict('senhmo.json', data)
        for each_stock_section in data:
            stock_diff = {}
            for each_ticker in each_stock_section:
                open_price_list = []
                stock_name = each_ticker
                for each_item in each_stock_section[each_ticker]:
                    for each2 in each_item:
                        open_price_list.append(each2['open_price'])
                stock_diff[stock_name] = open_price_list

        pprint(stock_diff)


if __name__ == '__main__':
    instance = Usage()
