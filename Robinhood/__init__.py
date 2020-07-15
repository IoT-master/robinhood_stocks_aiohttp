import random
from datetime import datetime, timedelta
from math import log

import jwt
import ujson

from Robinhood.basic_async_api import ApiOperations


class Robinhood(ApiOperations):
    from Robinhood.authentication import login, \
        respond_to_challenge

    from Robinhood.account import get_all_positions, \
        get_open_stock_positions, get_watchlist_by_name, get_dividends, get_total_dividends, \
        get_dividends_by_instrument, get_notifications, get_latest_notification, get_wire_transfers, get_margin_calls, \
        get_linked_bank_accounts, get_bank_account_info, unlink_bank_account, get_bank_transfers, \
        get_stock_loan_payments, get_margin_interest, get_subscription_fees, get_referrals, get_day_trades, \
        get_documents, download_document, load_basic_profile, load_user_profile

    from Robinhood.orders import cancel_all_crypto_orders, cancel_all_option_orders, cancel_all_stock_orders, \
        cancel_crypto_order, cancel_option_order, cancel_stock_order, find_stock_orders, get_all_crypto_orders, \
        get_all_open_crypto_orders, get_all_open_option_orders, get_all_open_stock_orders, get_all_option_orders, \
        get_all_stock_orders, get_crypto_order_info, get_option_order_info, get_stock_order_info, order, \
        order_buy_crypto_by_price, order_buy_crypto_by_quantity, order_buy_crypto_limit, order_buy_fractional_by_price, \
        order_buy_fractional_by_quantity, order_buy_limit, order_buy_market, order_buy_option_limit, \
        order_buy_option_stop_limit, order_buy_stop_limit, order_buy_stop_loss, order_option_credit_spread, \
        order_option_debit_spread, order_option_spread, order_sell_crypto_by_price, order_sell_crypto_by_quantity, \
        order_sell_crypto_limit, order_sell_fractional_by_price, order_sell_fractional_by_quantity, order_sell_limit, \
        order_sell_market, order_sell_option_limit, order_sell_option_stop_limit, order_sell_stop_limit, \
        order_sell_stop_loss

    from Robinhood.stocks import find_instrument_data, get_earnings, get_events, get_fundamentals, \
        get_instrument_by_url, get_instruments_by_symbols, get_latest_price, get_name_by_symbol, get_name_by_url, \
        get_news, get_popularity, get_pricebook_by_id, get_pricebook_by_symbol, get_quotes, get_ratings, get_splits, \
        get_stock_historicals, get_stock_quote_by_id, get_stock_quote_by_symbol, get_symbol_by_url

    from Robinhood.options import find_options_by_expiration, find_options_by_expiration_and_strike, \
        find_options_by_specific_profitability, find_tradable_options, get_aggregate_positions, \
        get_all_option_positions, get_chains, get_market_options, get_open_option_positions, get_option_market_data, \
        get_option_market_data_by_id

    from Robinhood.crypto import load_crypto_profile, get_crypto_positions, get_crypto_currency_pairs, get_crypto_info, \
        get_crypto_quote, get_crypto_quote_from_id, get_crypto_historicals

    from Robinhood.export import export_completed_option_orders, export_completed_stock_orders

    from Robinhood.profiles import load_account_profile, load_basic_profile, load_investment_profile, \
        load_portfolio_profile, load_security_profile, load_user_profile

    from Robinhood.markets import get_currency_pairs, get_markets, get_top_movers

    from Robinhood.custom import get_option_detail_from_position_filter, clear_screen, historical_filter, \
        get_option_detail_from_current_option_positions, historical_filter, open_option_positions_filter, \
        display_current_status_of_stock_list, get_stock_positions_from_account, \
        get_stock_and_option_positions_from_account, \
        get_list_of_instruments, get_current_status_of_stock_list, get_option_positions_from_account

    def __init__(self):
        super(Robinhood, self).__init__()

    async def id_for_stock(self, symbol):
        """Takes a stock ticker and returns the instrument id associated with the stock.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks instrument id.

        """
        symbol = symbol.upper().strip()

        url = 'https://api.robinhood.com/instruments/'
        payload = {'symbol': symbol}
        data = await self.custom_async_get_wild(url, 'indexzero', headers=self.default_header, params=payload)
        return self.data_filter(data, 'id')

    async def custom_async_get_wild(self, url, data_type='regular', headers=None, params=None, jsonify_data=True):
        if not jsonify_data:
            res = await self.async_get_wild(url, headers=headers, params=params, jsonify_data=False)
            return res
        res = await self.async_get_wild(url, headers=headers, params=params, jsonify_data=True)
        if data_type == 'results':
            return res['results']
        elif data_type == 'pagination':
            data = [res['results']]
            count = 0
            if 'next' in res:
                while res['next']:
                    res = await self.async_get_wild(res['next'], headers=headers, params=params, jsonify_data=True)
                    count += 1
                    assert count < 100
                    if 'results' in res:
                        for item in res['results']:
                            data.append(item)
            return data
        elif data_type == 'indexzero':
            data = res['results'][0]
            return data
        else:
            return res

    async def id_for_chain(self, symbol):
        """Takes a stock ticker and returns the chain id associated with a stocks option.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks options chain id.

        """
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return (None)

        payload = {'symbol': symbol}
        url = 'https://api.robinhood.com/instruments/'
        data = await self.async_get_wild(url, headers=self.default_header, params=payload, jsonify_data=True)
        return data['results'][0]['tradable_chain_id']

    async def id_for_group(self, symbol):
        """Takes a stock ticker and returns the id associated with the group.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks group id.

        """
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return (None)

        url = f'https://api.robinhood.com/options/chains/{await self.id_for_chain(symbol)}/'
        data = await self.async_get_wild(url, headers=self.default_header, jsonify_data=True)
        return data['underlying_instruments'][0]['id']

    async def id_for_option(self, symbol, expiration_date, strike, option_type):
        """Returns the id associated with a specific option order.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :param expiration_date: The expiration date as YYYY-MM-DD
        :type expiration_date: str
        :param strike: The strike price.
        :type strike: str
        :param option_type: Either call or put.
        :type option_type: str
        :returns:  A string that represents the stocks option id.

        """
        symbol = symbol.upper()

        payload = {
            'chain_symbol': symbol,
            'expiration_date': expiration_date,
            'strike_price': strike,
            'type': option_type,
            'state': 'active'
        }
        url = 'https://api.robinhood.com/options/instruments/'
        data = await self.custom_async_get_wild(url, 'pagination', params=payload)

        list_of_options = [
            item for item in data if item["expiration_date"] == expiration_date]
        if len(list_of_options) == 0:
            print(
                'Getting the option ID failed. Perhaps the expiration date is wrong format, or the strike price is wrong.')
            return None

        return list_of_options[0]['id']

    @staticmethod
    def filtering_options_body(each_option_owned, option_details, option_description):
        def calc_option_percentage(old, new):
            if new < old:
                return -(1 - new / old) * 100
            else:
                return (new / old - 1) * 100

        def calc_option_db(old, new):
            return log(new / old)

        return {
            'quantity': float(each_option_owned['quantity']),
            'created_at': each_option_owned['created_at'],
            'average_price': float(each_option_owned['average_price']),
            'option_id': each_option_owned['option_id'],
            'adjusted_mark_price': option_details['adjusted_mark_price'],
            'ask_price': option_details['ask_price'],
            'ask_size': option_details['ask_size'],
            'bid_price': option_details['bid_price'],
            'bid_size': option_details['bid_size'],
            'mark_price': float(option_details['mark_price']),
            'previous_close_price': option_details['previous_close_price'],
            'chance_of_profit_long': option_details['chance_of_profit_long'],
            'chance_of_profit_short': option_details['chance_of_profit_short'],
            'delta': option_details['delta'],
            'gamma': option_details['gamma'],
            'implied_volatility': option_details['implied_volatility'],
            'rho': option_details['rho'],
            'theta': option_details['theta'],
            'vega': option_details['vega'],
            'expiration_date': option_description['expiration_date'],
            'state': option_description['state'],
            'strike_price': float(option_description['strike_price']),
            'type': option_description['type'],
            'sellout_datetime': option_description['sellout_datetime'],
            'instrument_id': option_details['instrument'],
            'percent_gain': calc_option_percentage(float(each_option_owned['average_price']),
                                                   float(option_details['adjusted_mark_price']) * 100),
            'dB': calc_option_db(float(each_option_owned['average_price']),
                                 float(option_details['adjusted_mark_price']) * 100)
        }

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
            input_symbols = [
                comp for comp in input_symbols if type(comp) is str]
            for item in input_symbols:
                add_symbol(item)

        return symbols_list

    @staticmethod
    def is_token_valid(access_token, days_before_exp=1):
        time_stamp = jwt.decode(access_token, verify=False)['exp']
        real_time_stamp = datetime.fromtimestamp(time_stamp)
        return real_time_stamp - timedelta(days=days_before_exp) > datetime.now()

    @staticmethod
    def save_to_json_dict(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4, sort_keys=True))

    @staticmethod
    def save_to_json(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4))

    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r') as f:
            return ujson.loads(f.read())

    @staticmethod
    def data_filter(data, info):
        """Takes the data and extracts the value for the keyword that matches info.

        :param data: The data returned by request_get.
        :type data: dict or list
        :param info: The keyword to data_filter from the data.
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
            return data

    async def main(self):
        data = await self.login(self)
        print(data)
