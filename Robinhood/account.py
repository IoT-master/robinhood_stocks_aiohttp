import os

import Robinhood.urls as urls


async def get_all_positions(self, info=None):
    """Returns a list containing every position ever traded.

    :param self:
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

    return self.filter(data, info)


async def get_open_stock_positions(self, info=None):
    """Returns a list of stocks that are currently held.

    :param self:
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

    return self.filter(data, info)


async def get_all_watchlists(self, info=None):
    """Returns a list of all watchlists that have been created. Everone has a 'default' watchlist.

    :param self:
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of the watchlists. Keywords are 'url', 'user', and 'name'.

    """
    url = urls.watchlists()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
    return self.filter(data, info)


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
    return self.filter(data, info)


async def get_dividends(self, info=None):
    """Returns a list of dividend trasactions that include information such as the percentage rate,
    amount, shares of held stock, and date paid.

    :param self:
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each divident payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * id
                      * url
                      * account
                      * instrument
                      * amount
                      * rate
                      * position
                      * withholding
                      * record_date
                      * payable_date
                      * paid_at
                      * state
                      * nra_withholding
                      * drip_enabled

    """
    url = urls.dividends()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
    return self.filter(data, info)


async def get_total_dividends(self):
    """Returns a float number representing the total amount of dividends paid to the account.

    :returns: Total dollar amount of dividends paid to the account as a 2 precision float.

    """
    url = urls.dividends()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)

    dividend_total = 0
    for item in data:
        dividend_total += float(item['amount'])
    return dividend_total


@staticmethod
def get_dividends_by_instrument(instrument, dividend_data):
    """Returns a dictionary with three fields when given the instrument value for a stock

    :param instrument: The instrument to get the dividend data.
    :type instrument: str
    :param dividend_data: The information returned by get_dividends().
    :type dividend_data: list
    :returns: dividend_rate       -- the rate paid for a single share of a specified stock \
              total_dividend      -- the total dividend paid based on total shares for a specified stock \
              amount_paid_to_date -- total amount earned by account for this particular stock
    """
    # global dividend_data
    data = list(filter(lambda x: x['instrument'] == instrument, dividend_data))

    dividend = float(data[0]['rate'])
    total_dividends = float(data[0]['amount'])
    total_amount_paid = float(sum([float(d['amount']) for d in data]))

    return {
        'dividend_rate': "{0:.2f}".format(dividend),
        'total_dividend': "{0:.2f}".format(total_dividends),
        'amount_paid_to_date': "{0:.2f}".format(total_amount_paid)
    }


async def get_notifications(self, info=None):
    """Returns a list of notifications.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each notification. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.notifications()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
    return self.filter(data, info)


async def get_latest_notification(self):
    """Returns the time of the latest notification.

    :returns: Returns a dictionary of key/value pairs. But there is only one key, 'last_viewed_at'

    """
    url = urls.notifications(True)
    data = await self.async_get_wild(url, headers=self.default_header)
    return data


async def get_wire_transfers(self, info=None):
    """Returns a list of wire transfers.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each wire transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.wiretransfers()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
    return self.filter(data, info)


async def get_margin_calls(self, symbol=None):
    """Returns either all margin calls or margin calls for a specific stock.

    :param symbol: Will determine which stock to get margin calls for.
    :type symbol: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each margin call.

    """
    url = urls.margin()
    if symbol:
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return None
        payload = {'equity_instrument_id', self.id_for_stock(symbol)}
        data = await self.async_get_wild(url, headers=self.default_header, params=payload)
    else:
        data = await self.custom_async_get_wild(url, 'results', headers=self.default_header)

    return data


async def get_linked_bank_accounts(self, info=None):
    """Returns all linked bank accounts.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each bank.

    """
    url = urls.linked()
    data = await self.custom_async_get_wild(url, 'results', headers=self.default_header)
    return self.filter(data, info)


async def get_bank_account_info(self, bank_id, info=None):
    """Returns a single dictionary of bank information

    :param bank_id: The bank id.
    :type bank_id: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictinoary of key/value pairs for the bank. If info parameter is provided, \
    the value of the key that matches info is extracted.

    """
    url = urls.linked(bank_id)
    data = await self.async_get_wild(url, headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def unlink_bank_account(self, bank_id):
    """Unlinks a bank account.

    :param bank_id: The bank id.
    :type bank_id: str
    :returns: Information returned from post request.

    """
    url = urls.linked(bank_id, True)
    data = await self.async_post_wild(url, headers=self.default_header, jsonify_data=True)
    return data


async def get_bank_transfers(self, info=None):
    """Returns all bank transfers made for the account.

    :param info: Will filter the results to get a specific value. 'direction' gives if it was deposit or withdrawl.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.banktransfers()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_stock_loan_payments(self, info=None):
    """Returns a list of loan payments.

    :param self:
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.stockloan()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_margin_interest(self, info=None):
    """Returns a list of margin interest.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each interest. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.margininterest()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_subscription_fees(self, info=None):
    """Returns a list of subscription fees.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each fee. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.subscription()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_referrals(self, info=None):
    """Returns a list of referrals.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each referral. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.referral()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_day_trades(self, info=None):
    """Returns recent day trades.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each day trade. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    account = self.load_account_profile('account_number')
    url = urls.daytrades(account)
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def get_documents(self, info=None):
    """Returns a list of documents that have been released by Robinhood to the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each document. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.documents()
    data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, jsonify_data=True)
    return self.filter(data, info)


async def download_document(self, url, name=None, dirpath=None):
    """Downloads a document and saves as it as a PDF. If no name is given, document is saved as
    the name that Robinhood has for the document. If no directory is given, document is saved in the root directory of code.

    :param url: The url of the document. Can be found by using get_documents(info='download_url').
    :type url: str
    :param name: The name to save the document as.
    :type name: Optional[str]
    :param dirpath: The directory of where to save the document.
    :type dirpath: Optional[str]
    :returns: Returns the data from the get request.

    """
    data = self.request_document(url)

    print('Writing PDF...')
    if not name:
        name = url[36:].split('/', 1)[0]

    if dirpath:
        directory = dirpath
    else:
        directory = 'robin_documents/'

    filename = directory + name + ' .pdf'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    open(filename, 'wb').write(data.content)
    print('Done - Wrote file {}.pdf to {}'.format(name, os.path.abspath(filename)))
    return data


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
    return self.filter(data, info)


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
    return self.filter(data, info)


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
    return self.filter(data, info)


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
    return self.filter(data, info)


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
    return self.filter(data, info)
