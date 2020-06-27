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
    return self.data_filter(data, info)


async def load_basic_profile(self, info=None):
    """Gets the information associated with the personal profile,
    such as phone number, city, marital status, and date of birth.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. If a string \
    is passed in to the info parameter, then the function will return a string \
    corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.basic_profile()
    data = await self.custom_async_get_wild(url, headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)


async def load_investment_profile(self, info=None):
    """Gets the information associated with the investment profile.
    These are the answers to the questionaire you filled out when you made your profile.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.investment_profile()
    data = await self.custom_async_get_wild(url, headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)


async def load_portfolio_profile(self, info=None):
    """Gets the information associated with the portfolios profile,
    such as withdrawable amount, market value of account, and excess margin.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.portfolio_profile()
    data = await self.custom_async_get_wild(url, 'indexzero', headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)


async def load_security_profile(self, info=None):
    """Gets the information associated with the security profile.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.security_profile()
    data = await self.custom_async_get_wild(url, headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)


async def load_user_profile(self, info=None):
    """Gets the information associated with the user profile,
    such as username, email, and links to the urls for other profiles.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.

    """
    url = urls.user_profile()
    data = await self.custom_async_get_wild(url, headers=self.default_header, jsonify_data=True)
    return self.data_filter(data, info)
