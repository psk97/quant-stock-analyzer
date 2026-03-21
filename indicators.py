import numpy as np

def add_indicators(data):
    # Moving Averages
    data['MA50'] = data['Close'].rolling(50).mean()
    data['MA200'] = data['Close'].rolling(200).mean()

    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Returns & Volatility
    data['Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Return'].rolling(30).std()

    return data
