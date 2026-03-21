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
