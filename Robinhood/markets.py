import Robinhood.urls as urls


async def get_top_movers(self, direction, info=None):
    """Returns a list of the top movers up or down for the day.

    :param direction: The direction of movement either 'up' or 'down'
    :type direction: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        direction = direction.lower().strip()
    except AttributeError as message:
        print(message)
        return None

    if direction != 'up' and direction != 'down':
        print('Error: direction must be "up" or "down"')
        return [None]

    url = urls.movers()
    payload = {'direction': direction}
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, params=payload,
                                            jsonify_data=True)
    return self.data_filter(data, info)


async def get_markets(self, info=None):
    """Returns a list of available markets.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each market. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.markets()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)


async def get_currency_pairs(self, info=None):
    """Returns currency pairs

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each currency pair. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """

    url = urls.currency()
    data = await self.custom_async_get_wild(url, 'results', headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)
