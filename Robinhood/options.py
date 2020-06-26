import Robinhood.urls as urls
from Robinhood.authentication import Authorization


class Options(Authorization):
    def __init__(self):
        super(Options, self).__init__()

    async def get_aggregate_positions(self, info=None):
        """Collapses all option orders for a stock into a single dictionary.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        url = urls.aggregate()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return Options.filter(data, info)

    async def get_market_options(self, info=None):
        """Returns a list of all options.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        url = urls.option_orders()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return Options.filter(data, info)

    async def get_all_option_positions(self, info=None):
        """Returns all option positions ever held for the account.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        url = urls.option_positions()
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header)
        return Options.filter(data, info)

    async def get_open_option_positions(self, info=None):
        """Returns all open option positions for the account.

        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        url = urls.option_positions()
        payload = {'nonzero': 'True'}
        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, params=payload)
        return Options.filter(data, info)

    async def get_chains(self, symbol, info=None):
        """Returns the chain information of an option.

        :param symbol: The ticker of the stock.
        :type symbol: str
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a dictionary of key/value pairs for the option. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return None
        url = f'https://api.robinhood.com/options/chains/{await self.id_for_chain(symbol)}/'
        data = await self.custom_async_get_wild(url, headers=self.default_header)
        return Options.filter(data, 'expiration_dates')

    async def find_tradable_options(self, symbol, expiration_date=None, strike_price=None, option_type=None, info=None):
        """Returns a list of all available options for a stock.

        :param symbol: The ticker of the stock.
        :type symbol: str
        :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
        :type expiration_date: str
        :param strike_price: Represents the strike price of the option.
        :type strike_price: str
        :param option_type: Can be either 'call' or 'put' or left blank to get both.
        :type option_type: Optional[str]
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for all calls of the stock. If info parameter is provided, \
        a list of strings is returned where the strings are the value of the key that matches info.

        """

        symbol = symbol.upper().strip()

        url = urls.option_instruments()

        payload = {'chain_id': await self.id_for_chain(symbol),
                   'chain_symbol': symbol,
                   'state': 'active'}

        if expiration_date:
            payload['expiration_date'] = expiration_date
        if strike_price:
            payload['strike_price'] = strike_price
        if option_type:
            payload['type'] = option_type

        data = await self.custom_async_get_wild(url, 'pagination', headers=self.default_header, params=payload)
        return Options.filter(data, info)

    async def find_options_by_expiration_and_strike(self, input_symbols, expiration_date, strike_price,
                                                    option_type=None, info=None):
        """Returns a list of all the option orders that match the seach parameters

        :param input_symbols: The ticker of either a single stock or a list of stocks.
        :type input_symbols: str
        :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
        :type expiration_date: str
        :param strike_price: Represents the strike price to filter for.
        :type strike_price: str
        :param option_type: Can be either 'call' or 'put' or leave blank to get both.
        :type option_type: Optional[str]
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

        """
        try:
            symbols = self.inputs_to_set(input_symbols)
            if option_type:
                option_type = option_type.lower().strip()
        except AttributeError as message:
            print(message)
            return [None]

        data = []
        for symbol in symbols:
            all_options = await self.find_tradable_options(symbol, expiration_date, strike_price, option_type, None)
            filtered_options = [item for item in all_options if item.get("expiration_date") == expiration_date]

            for item in filtered_options:
                marketData = self.get_option_market_data_by_id(item['id'])
                item.update(marketData)

            data.extend(filtered_options)

        return self.filter(data, info)

    async def find_options_by_specific_profitability(self, input_symbols, expiration_date=None, strike_price=None,
                                                     option_type=None,
                                                     type_profit="chance_of_profit_short", profit_floor=0.0,
                                                     profit_ceiling=1.0,
                                                     info=None):
        """Returns a list of option market data for several stock tickers that match a range of profitability.

        :param input_symbols: May be a single stock ticker or a list of stock tickers.
        :type input_symbols: str or list
        :param expiration_date: Represents the expiration date in the format YYYY-MM-DD. Leave as None to get all available dates.
        :type expiration_date: str
        :param strike_price: Represents the price of the option. Leave as None to get all available strike prices.
        :type strike_price: str
        :param option_type: Can be either 'call' or 'put' or leave blank to get both.
        :type option_type: Optional[str]
        :param type_profit: Will either be "chance_of_profit_short" or "chance_of_profit_long".
        :type type_profit: str
        :param profit_floor: The lower percentage on scale 0 to 1.
        :type profit_floor: int
        :param profit_ceiling: The higher percentage on scale 0 to 1.
        :type profit_ceiling: int
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for all stock option market data. \
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

        """
        symbols = self.inputs_to_set(input_symbols)
        data = []

        if type_profit != "chance_of_profit_short" and type_profit != "chance_of_profit_long":
            print("Invalid string for 'typeProfit'. Defaulting to 'chance_of_profit_short'.")
            type_profit = "chance_of_profit_short"

        for symbol in symbols:
            temp_data = await self.find_tradable_options(symbol, expiration_date, strike_price, option_type, info=None)
            for option in temp_data:
                if expiration_date and option.get("expiration_date") != expiration_date:
                    continue

                market_data = await self.get_option_market_data_by_id(option['id'])
                option.update(market_data)

                float_value = float(option[type_profit])
                if float_value >= profit_floor and float_value <= profit_ceiling:
                    data.append(option)

        return Options.filter(data, info)

    async def get_option_market_data_by_id(self, id, info=None):
        """Returns the option market data for a stock, including the greeks,
        open interest, change of profit, and adjusted mark price.

        :param id: The id of the stock.
        :type id: str
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a dictionary of key/value pairs for the stock. \
        If info parameter is provided, the value of the key that matches info is extracted.

        """
        url = urls.marketdata_options(id)
        data = await self.async_get_wild(url, headers=self.default_header, jsonify_data=True)

        if not data:
            data = {
                'adjusted_mark_price': '',
                'ask_price': '',
                'ask_size': '',
                'bid_price': '',
                'bid_size': '',
                'break_even_price': '',
                'high_price': '',
                'instrument': '',
                'last_trade_price': '',
                'last_trade_size': '',
                'low_price': '',
                'mark_price': '',
                'open_interest': '',
                'previous_close_date': '',
                'previous_close_price': '',
                'volume': '',
                'chance_of_profit_long': '',
                'chance_of_profit_short': '',
                'delta': '',
                'gamma': '',
                'implied_volatility': '',
                'rho': '',
                'theta': '',
                'vega': '',
                'high_fill_rate_buy_price': '',
                'high_fill_rate_sell_price': '',
                'low_fill_rate_buy_price': '',
                'low_fill_rate_sell_price': ''
            }

        return Options.filter(data, info)

    async def get_option_market_data(self, input_symbols, expiration_date, strike_price, option_type, info=None):
        """Returns the option market data for the stock option, including the greeks,
        open interest, change of profit, and adjusted mark price.

        :param input_symbols: The ticker of the stock.
        :type input_symbols: str
        :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
        :type expiration_date: str
        :param strike_price: Represents the price of the option.
        :type strike_price: str
        :param option_type: Can be either 'call' or 'put'.
        :type option_type: str
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a dictionary of key/value pairs for the stock. \
        If info parameter is provided, the value of the key that matches info is extracted.

        """

        symbols = self.inputs_to_set(input_symbols)
        if option_type:
            option_type = option_type.lower().strip()

        data = []
        for symbol in symbols:
            option_id = await self.id_for_option(symbol, expiration_date, strike_price, option_type)
            market_data = await self.get_option_market_data_by_id(option_id)
            data.append(market_data)

        return Options.filter(data, info)

    @staticmethod
    def inputs_to_set(input_symbols):
        """Takes in the parameters passed to *args and puts them in a set and a list.
        The set will make sure there are no duplicates, and then the list will keep
        the original order of the input.

        :param input_symbols: A list, dict, or tuple of stock tickers.
        :type input_symbols: list or dict or tuple or str
        :returns:  A list of strings that have been capitalized and stripped of white space.

        """

        symbols_list = []
        symbols_set = set()

        def add_symbol(symbol):
            symbol = symbol.upper().strip()
            if symbol not in symbols_set:
                symbols_set.add(symbol)
                symbols_list.append(symbol)

        if type(input_symbols) is str:
            add_symbol(input_symbols)
        elif type(input_symbols) is list or type(input_symbols) is tuple or type(input_symbols) is set:
            input_symbols = [comp for comp in input_symbols if type(comp) is str]
            for item in input_symbols:
                add_symbol(item)

        return symbols_list

    @staticmethod
    def round_price(price):
        """Takes a price and rounds it to an appropriate decimal place that Robinhood will accept.

        :param price: The input price to round.
        :type price: float or int
        :returns: The rounded price as a float.

        """
        price = float(price)
        if price <= 1e-2:
            return_price = round(price, 6)
        elif price < 1e0:
            return_price = round(price, 4)
        else:
            return_price = round(price, 2)

        return return_price

    async def find_options_by_expiration(self, input_symbols, expiration_date, option_type=None, info=None):
        """Returns a list of all the option orders that match the seach parameters

        :param input_symbols: The ticker of either a single stock or a list of stocks.
        :type input_symbols: str
        :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
        :type expiration_date: str
        :param option_type: Can be either 'call' or 'put' or leave blank to get both.
        :type option_type: Optional[str]
        :param info: Will filter the results to get a specific value.
        :type info: Optional[str]
        :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
        If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

        """
        try:
            symbols = Options.inputs_to_set(input_symbols)
            if option_type:
                option_type = option_type.lower().strip()
        except AttributeError as message:
            print(message)
            return [None]

        data = []
        for symbol in symbols:
            all_options = await self.find_tradable_options(symbol, expiration_date, None, option_type, None)
            filtered_options = [item for item in all_options if item.get("expiration_date") == expiration_date]

            for item in filtered_options:
                market_data = await self.get_option_market_data_by_id(item['id'])
                item.update(market_data)

            data.extend(filtered_options)

        return Options.filter(data, info)

    async def main(self):
        await self.login()
        # data = await self.find_options_by_expiration('TSLA', expiration_date='2020-10-16', option_type='call')
        data = await self.get_aggregate_positions()
        self.save_to_json('senhmo.json', data)


if __name__ == '__main__':
    instance = Options()
