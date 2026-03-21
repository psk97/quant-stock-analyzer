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

    st.subheader("Metrics")
    st.write(metrics)

    fig1 = plt.figure()
    plt.plot(data['Close'])
    plt.title("Stock Price")
    st.pyplot(fig1)

    fig2 = plt.figure()
    plt.plot(data['Portfolio'])
    plt.title("Portfolio Value")
    st.pyplot(fig2)
