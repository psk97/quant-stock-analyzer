# ==============================
# Quantitative Stock Analysis & Backtesting System
# ==============================

# -------- requirements.txt --------
# yfinance
# pandas
# numpy
# matplotlib
# streamlit

# -------- data_loader.py --------
import yfinance as yf
import pandas as pd

def load_data(ticker, period="2y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    data.dropna(inplace=True)
    return data

# -------- indicators.py --------
import numpy as np

def add_indicators(data):
    data['MA50'] = data['Close'].rolling(50).mean()
    data['MA200'] = data['Close'].rolling(200).mean()

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    data['Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Return'].rolling(30).std()

    return data

# -------- strategy.py --------

def generate_signals(data):
    data['Signal'] = 0
    data.loc[data['MA50'] > data['MA200'], 'Signal'] = 1
    return data

# -------- backtester.py --------

def backtest(data, initial_cash=10000):
    cash = initial_cash
    position = 0
    portfolio_values = []

    for i in range(len(data)):
        price = data['Close'].iloc[i]
        signal = data['Signal'].iloc[i]

        if signal == 1 and cash > 0:
            position = cash / price
            cash = 0
        elif signal == 0 and position > 0:
            cash = position * price
            position = 0

        portfolio_values.append(cash + position * price)

    data['Portfolio'] = portfolio_values
    return data

# -------- metrics.py --------
import numpy as np

def calculate_metrics(data):
    returns = data['Portfolio'].pct_change().dropna()
    sharpe = returns.mean() / returns.std() * np.sqrt(252)

    cumulative = data['Portfolio']
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_dd = drawdown.min()

    return {
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Final Value": cumulative.iloc[-1]
    }

# -------- main.py --------
import matplotlib.pyplot as plt
from data_loader import load_data
from indicators import add_indicators
from strategy import generate_signals
from backtester import backtest
from metrics import calculate_metrics


def run_analysis(ticker="AAPL"):
    data = load_data(ticker)
    data = add_indicators(data)
    data = generate_signals(data)
    data = backtest(data)

    metrics = calculate_metrics(data)

    print("Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    plt.figure()
    plt.plot(data['Close'], label='Price')
    plt.plot(data['MA50'], label='MA50')
    plt.plot(data['MA200'], label='MA200')
    plt.legend()
    plt.title(f"{ticker} Analysis")
    plt.show()

    plt.figure()
    plt.plot(data['Portfolio'], label='Portfolio Value')
    plt.legend()
    plt.title("Backtest Performance")
    plt.show()


if __name__ == "__main__":
    run_analysis("AAPL")

# -------- dashboard/app.py --------
import streamlit as st
import matplotlib.pyplot as plt
from data_loader import load_data
from indicators import add_indicators
from strategy import generate_signals
from backtester import backtest
from metrics import calculate_metrics

st.title("Quant Stock Analyzer")

ticker = st.text_input("Enter Stock Ticker", "AAPL")

if st.button("Run Analysis"):
    data = load_data(ticker)
    data = add_indicators(data)
    data = generate_signals(data)
    data = backtest(data)

    metrics = calculate_metrics(data)

    st.write(metrics)

    fig1 = plt.figure()
    plt.plot(data['Close'])
    plt.title("Price")
    st.pyplot(fig1)

    fig2 = plt.figure()
    plt.plot(data['Portfolio'])
    plt.title("Portfolio Value")
    st.pyplot(fig2)
