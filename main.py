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

    print(f"\n=== {ticker} Results ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # Price + Indicators
    plt.figure()
    plt.plot(data['Close'], label='Price')
    plt.plot(data['MA50'], label='MA50')
    plt.plot(data['MA200'], label='MA200')
    plt.legend()
    plt.title(f"{ticker} Price & Moving Averages")
    plt.show()

    # Portfolio performance
    plt.figure()
    plt.plot(data['Portfolio'], label='Portfolio Value')
    plt.legend()
    plt.title("Backtest Performance")
    plt.show()

if __name__ == "__main__":
    run_analysis("AAPL")
