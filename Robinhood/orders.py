import aiohttp
import ujson

import Robinhood.urls as urls
from Robinhood.authentication import Authorization


class Orders(Authorization):
    async def get_all_option_orders(self, info=None):
        """Returns a list of all the option orders that have been processed for the account.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for each option order. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        url = urls.option_orders()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return self.filter(data, info)

    async def main(self):
        await self.login()
        data = await self.get_all_option_orders()
        self.save_to_json_dict('senhmo.json', data)

if __name__=='__main__':
    instance = Orders()