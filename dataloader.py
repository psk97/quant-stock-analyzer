import yfinance as yf

def load_data(ticker, period="2y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    data.dropna(inplace=True)
    return data
