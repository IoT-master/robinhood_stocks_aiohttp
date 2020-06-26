from Robinhood.helper import ApiOperations

import jwt
import random
from datetime import datetime, timedelta
import ujson


class Robinhood(ApiOperations):
    from Robinhood.authentication import login, custom_async_get_wild, \
        respond_to_challenge, id_for_chain, id_for_group, id_for_stock, id_for_option
    from Robinhood.account import get_all_positions, \
        get_open_stock_positions, get_watchlist_by_name
    from Robinhood.orders import get_all_option_orders

    def __init__(self):
        super(Robinhood, self).__init__()

    @staticmethod
    def generate_device_token():
        """This function will generate a token used when logging on.

        :returns: A string representing the token.

        """
        rands = []
        for i in range(0, 16):
            r = random.random()
            rand = 4294967296.0 * r
            rands.append((int(rand) >> ((3 & i) << 3)) & 255)

        hexa = []
        for i in range(0, 256):
            hexa.append(str(hex(i + 256)).lstrip("0x").rstrip("L")[1:])

        ids = ""
        for i in range(0, 16):
            ids += hexa[rands[i]]

            if (i == 3) or (i == 5) or (i == 7) or (i == 9):
                ids += "-"

        return ids

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
    def is_token_valid(access_token, minutes_before_exp=30):
        time_stamp = jwt.decode(access_token, verify=False)['exp']
        real_time_stamp = datetime.fromtimestamp(time_stamp)
        return real_time_stamp - timedelta(minutes=minutes_before_exp) > datetime.now()

    @staticmethod
    def save_to_json_dict(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4, sort_keys=True))

    @staticmethod
    def save_to_json(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4))

    @staticmethod
    def filter(data, info):
        """Takes the data and extracts the value for the keyword that matches info.

        :param data: The data returned by request_get.
        :type data: dict or list
        :param info: The keyword to filter from the data.
        :type info: str
        :returns:  A list or string with the values that correspond to the info keyword.

        """
        if data is None:
            return data
        elif data == [None]:
            return ([])
        elif type(data) == list:
            if len(data) == 0:
                return ([])
            compare_dict = data[0]
            none_type = []
        elif type(data) == dict:
            compare_dict = data
            none_type = None

        if info is not None:
            if info in compare_dict and type(data) == list:
                return [x[info] for x in data]
            elif info in compare_dict and type(data) == dict:
                return data[info]
            else:
                return none_type
        else:
            return (data)

    async def main(self):
        # data = await self.login()
        data = testy()
        print(data)


if __name__ == '__main__':
    def testy():
        return 'hi'


    ins = Robinhood()
