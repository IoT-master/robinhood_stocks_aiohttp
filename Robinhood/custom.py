import os
from math import log
from subprocess import call
from time import sleep

from tqdm import tqdm


@staticmethod
def clear_screen():
    call('clear' if os.name == 'posix' else 'cls')


@staticmethod
def historical_filter(data, key_word='begins_at', value_word='open_price'):
    stock_diff = {}
    for each_stock_section in data:
        for each_ticker in each_stock_section:
            open_price_list = []
            stock_name = each_ticker
            for each_item in each_stock_section[each_ticker]:
                for each2 in each_item:
                    open_price_list.append(
                        {each2[key_word]: each2[value_word]})
            stock_diff[stock_name] = open_price_list
    return stock_diff


@staticmethod
def open_option_positions_filter(data, key_word, value_word):
    stock_diff = {}
    for empty_index in data:
        for each_stock_section in empty_index:
            key_word_value = each_stock_section[key_word]
            if key_word_value not in stock_diff:
                stock_diff[key_word_value] = [
                    dict(map(lambda x: (x, each_stock_section[x]), value_word))]
            else:
                stock_diff[key_word_value].append(
                    dict(map(lambda x: (x, each_stock_section[x]), value_word)))
    return stock_diff


async def get_option_detail_from_position_filter(self, oop_filter):
    for ticker_name in oop_filter:
        for index, each_item in enumerate(oop_filter[ticker_name]):
            oop_filter[ticker_name][index]['option_details'] = await self.get_option_market_data_by_id(
                each_item['option_id'])


async def get_option_detail_from_current_option_positions(self):
    """
    This API returns all the OPEN option positions that you have and associates it with a ticker symbols
    :param self:
    :return: A dict with with OPEN option positions with the corresponding ticker symbols
    """
    data = await self.get_open_option_positions()
    oop_filter = self.open_option_positions_filter(data, key_word='chain_symbol',
                                                   value_word=['average_price', 'quantity', 'type', 'option_id'])
    await self.get_option_detail_from_position_filter(oop_filter)
    return data


async def display_current_status_of_stock_list(self, stock_list, sleep_time=.5):
    def calc_stock_percentage(old, new):
        if new < old:
            return -(1 - new / old) * 100
        else:
            return (new / old - 1) * 100

    while True:
        data = await self.get_quotes(stock_list)
        data_to_screen = dict(map(lambda x: (x['symbol'], {'bid': float(x['bid_price']),
                                                           'ask': float(x['ask_price']),
                                                           'adjusted_previous_close': float(
                                                               x['adjusted_previous_close']),
                                                           'last': float(x['last_trade_price']),
                                                           'trading': x['trading_halted'],
                                                           'percent': calc_stock_percentage(
                                                               float(
                                                                   x['adjusted_previous_close']),
                                                               float(x['last_trade_price'])),
                                                           'dB': 0 if (float(x['last_trade_price'])) / float(
                                                               x['adjusted_previous_close']) == 0 else log(
                                                               (float(x['last_trade_price'])) / float(
                                                                   x['adjusted_previous_close']))
                                                           }), data))
        for each_ticker in data_to_screen:
            stats = data_to_screen[each_ticker]
            print(
                f"{each_ticker.rjust(20, '*')}: bid: {stats['bid']:8.2f}, ask: {stats['ask']:8.2f}, last {stats['last']:8.2f}, %: {stats['percent']:6.2f}, dB:{stats['dB']:6.2f}")
        sleep(sleep_time)
        self.clear_screen()


async def get_current_status_of_stock_list(self, stock_list):
    def calc_stock_percentage(old, new, extend_new):
        if extend_new:
            up_change = float(extend_new)
        else:
            up_change = new
        if up_change < old:
            return -(1 - up_change / old) * 100
        else:
            return (up_change / old - 1) * 100

    stock_quotes = await self.get_quotes(stock_list)
    filtered_stock_quotes = filter(lambda x: x, stock_quotes)
    data_to_screen = dict(map(lambda x: (x['symbol'], {'bid': float(x['bid_price']),
                                                       'ask': float(x['ask_price']),
                                                       'adjusted_previous_close': float(
                                                           x['adjusted_previous_close']),
                                                       'last': float(x['last_trade_price']),
                                                       'trading': x['trading_halted'],
                                                       'percent': calc_stock_percentage(
                                                           float(
                                                               x['adjusted_previous_close']),
                                                           float(
                                                               x.get('last_extended_hours_trade_price', x['last_trade_price'])),
                                                           x['last_extended_hours_trade_price']),
                                                       'dB': 0 if (float(x.get('last_extended_hours_trade_price', x['last_trade_price']))) / float(
                                                           x['adjusted_previous_close']) == 0 else log(
                                                           (float(x.get('last_extended_hours_trade_price', x['last_trade_price']))) / float(
                                                               x['adjusted_previous_close'])),
                                                       'extended': float(x['last_extended_hours_trade_price']) if x[
                                                           'last_extended_hours_trade_price'] else float(
                                                           x['last_trade_price'])
                                                       }), filtered_stock_quotes))
    return data_to_screen


async def get_list_of_instruments(self, response_body):
    stock_ticker_dict = {}
    for each_position in tqdm(response_body[0]):
        stock_ticker = await self.get_symbol_by_url(each_position['instrument'])
        if stock_ticker:
            each_position['ticker'] = stock_ticker
            stock_ticker_dict[stock_ticker] = {'average_buy_price': each_position['average_buy_price'],
                                               'quantity': each_position['quantity'],
                                               'url': each_position['url'],
                                               'instrument': each_position['instrument'],
                                               'created_at': each_position['created_at']
                                               }
    return stock_ticker_dict


async def get_stock_positions_from_account(self):
    stock_positions = await self.get_open_stock_positions()
    stock_ticker_dict = await self.get_list_of_instruments(stock_positions)
    owned_stock_ticker_list = [
        each_stock_ticker for each_stock_ticker in stock_ticker_dict]
    owned_stocker_ticker_statii = await self.get_current_status_of_stock_list(owned_stock_ticker_list)
    for each_stock_ticker in stock_ticker_dict:
        stock_ticker_dict[each_stock_ticker]['status'] = owned_stocker_ticker_statii[each_stock_ticker]

    return stock_ticker_dict


async def _get_stock_and_option_positions_from_account(self):
    #TODO Combine to one whole list of instruments
    stock_positions = await self.get_open_stock_positions()
    stock_ticker_dict = await self.get_list_of_instruments(stock_positions)
    option_positions = await self.get_option_positions_from_account()
    option_ticker_dict = await self.get_list_of_instruments(option_positions)
    owned_stock_ticker_list = [
        each_stock_ticker for each_stock_ticker in stock_ticker_dict]
    option_positions = await self.get_option_positions_from_account()

    owned_stocker_ticker_statii = await self.get_current_status_of_stock_list(owned_stock_ticker_list)
    for each_stock_ticker in stock_ticker_dict:
        stock_ticker_dict[each_stock_ticker]['status'] = owned_stocker_ticker_statii[each_stock_ticker]

    return stock_ticker_dict

async def get_option_positions_from_account(self):
    data = await self.get_open_option_positions()
    options_dict = {}
    for each_option in tqdm(data[0]):
        option_id = each_option['option_id']
        greeks_dict = await self.get_option_market_data_by_id(option_id)
        instrument_id = greeks_dict['instrument']
        option_detail = await self.async_get_wild(instrument_id, headers=self.default_header, jsonify_data=True)
        ticker_symbol = each_option['chain_symbol']
        if ticker_symbol not in options_dict:
            options_dict[ticker_symbol] = [self.filtering_options_body(
                each_option, greeks_dict, option_detail)]
        else:
            options_dict[ticker_symbol].append(self.filtering_options_body(
                each_option, greeks_dict, option_detail))
    return options_dict
