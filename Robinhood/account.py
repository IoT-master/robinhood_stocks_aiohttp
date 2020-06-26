import aiohttp
import ujson

import Robinhood.urls as urls
from Robinhood.authentication import Authorization


class Accounts(Authorization):

    def __init__(self):
        super(Accounts, self).__init__()

    async def get_all_positions(self, info=None):
        """Returns a list containing every position ever traded.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: [list] Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.
        :Dictionary Keys: * url
                          * instrument
                          * account
                          * account_number
                          * average_buy_price
                          * pending_average_buy_price
                          * quantity
                          * intraday_average_buy_price
                          * intraday_quantity
                          * shares_held_for_buys
                          * shares_held_for_sells
                          * shares_held_for_stock_grants
                          * shares_held_for_options_collateral
                          * shares_held_for_options_events
                          * shares_pending_from_options_events
                          * updated_at
                          * created_at

        """
        url = urls.positions()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)

        return Authorization.filter(data, info)

    async def get_open_stock_positions(self, info=None):
        """Returns a list of stocks that are currently held.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: [list] Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.
        :Dictionary Keys: * url
                          * instrument
                          * account
                          * account_number
                          * average_buy_price
                          * pending_average_buy_price
                          * quantity
                          * intraday_average_buy_price
                          * intraday_quantity
                          * shares_held_for_buys
                          * shares_held_for_sells
                          * shares_held_for_stock_grants
                          * shares_held_for_options_collateral
                          * shares_held_for_options_events
                          * shares_pending_from_options_events
                          * updated_at
                          * created_at

        """
        url = urls.positions()
        payload = {'nonzero': 'true'}
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, params=payload)

        return Accounts.filter(data, info)

    async def get_all_watchlists(self, info=None):
        """Returns a list of all watchlists that have been created. Everone has a 'default' watchlist.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of the watchlists. Keywords are 'url', 'user', and 'name'.

        """
        url = urls.watchlists()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return Accounts.filter(data, info)

    async def get_watchlist_by_name(self, name='Default', info=None):
        """Returns a list of information related to the stocks in a single watchlist.

        :param name: The name of the watchlist to get data from.
        :type name: Optional[str]
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries that contain the instrument urls and a url that references itself.

        """
        url = urls.watchlists(name)
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return Accounts.filter(data, info)

    async def main(self):
        await self.login()
        data = await self.get_all_positions()
        self.save_to_json_dict('senhmo.json', data)


if __name__ == '__main__':
    instance = Accounts()
