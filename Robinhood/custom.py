import os
from subprocess import call
from time import sleep


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
                    open_price_list.append({each2[key_word]: each2[value_word]})
            stock_diff[stock_name] = open_price_list
    return stock_diff


@staticmethod
def open_option_positions_filter(data, key_word, value_word):
    stock_diff = {}
    for empty_index in data:
        for each_stock_section in empty_index:
            key_word_value = each_stock_section[key_word]
            if key_word_value not in stock_diff:
                stock_diff[key_word_value] = [dict(map(lambda x: (x, each_stock_section[x]), value_word))]
            else:
                stock_diff[key_word_value].append(dict(map(lambda x: (x, each_stock_section[x]), value_word)))
    return stock_diff


async def get_option_detail_from_position_filter(self, oop_filter):
    for ticker_name in oop_filter:
        for index, each_item in enumerate(oop_filter[ticker_name]):
            oop_filter[ticker_name][index]['option_details'] = await self.get_option_market_data_by_id(
                each_item['option_id'])


async def get_option_detail_from_current_option_positions(self):
    data = await self.get_open_option_positions()
    oop_filter = self.open_option_positions_filter(data, key_word='chain_symbol',
                                                   value_word=['average_price', 'quantity', 'type', 'option_id'])
    await self.get_option_detail_from_position_filter(oop_filter)
    return data


async def display_current_status_of_stock_list(self, stock_list, sleep_time=.5):
    while True:
        data = await self.get_quotes(stock_list)
        data_to_screen = dict(map(lambda x: (x['symbol'], {'bid_price': x['bid_price'],
                                                           'ask_price': x['ask_price'],
                                                           'adjusted_previous_close': x['adjusted_previous_close'],
                                                           'last_trade_price': x['last_trade_price'],
                                                           'trading_halted': x['trading_halted'],
                                                           }), data))
        for each_ticker in data_to_screen:
            print(data_to_screen[each_ticker])
        sleep(sleep_time)
        self.clear_screen()
