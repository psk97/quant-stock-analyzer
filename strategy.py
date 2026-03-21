def generate_signals(data):
    data['Signal'] = 0
    data.loc[data['MA50'] > data['MA200'], 'Signal'] = 1
    return data
