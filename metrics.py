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
