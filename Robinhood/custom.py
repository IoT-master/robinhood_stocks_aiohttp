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


def open_option_positions_filter(data, key_word='chain_symbol',
                                 value_word=['average_price', 'quantity', 'type', 'option']):
    stock_diff = {}
    for empty_index in data:
        for each_stock_section in empty_index:
            key_word_value = each_stock_section[key_word]
            if key_word_value not in stock_diff:
                stock_diff[key_word_value] = [dict(map(lambda x: (x, each_stock_section[x]), value_word))]
            else:
                stock_diff[key_word_value].append(dict(map(lambda x: (x, each_stock_section[x]), value_word)))
    return stock_diff
