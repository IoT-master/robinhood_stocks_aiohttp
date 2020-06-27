import Robinhood.urls as urls


async def load_account_profile(self, info=None):
    """Gets the information associated with the accounts profile,including day
    trading information and cash being held by Robinhood.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.account_profile()
    data = await self.custom_async_get_wild(url, 'indexzero', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)
