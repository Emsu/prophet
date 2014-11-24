from collections import defaultdict

import pandas as pd
from prophet.portfolio import Portfolio
from prophet.exceptions import ProphetException
from six import iteritems


class BackTest(pd.Series):
    """ Timeseries data representing portfolio value over the backtest period.

    Note:
        Subclasses :class:`pd.Series` in v0.1
    """

    def get_daily_returns(self):
        """ Computes Series of daily returns

        Returns:
            pd.Series: Series of returns normalized to 0
        """
        # Portfolio values / yesterday's portfolio values
        returns = self / self.shift(1)
        returns0 = returns - 1.0
        # Fill day one with 0.0 return
        return returns0.fillna(0.0)

    def normalize1(self):
        """ Normalizes portfolio values to 1

        Returns:
            pd.Series: Series of portfolio values normalized to 1
        """

        return self / self.iloc[1]

    def normalize0(self):
        """ Normalizes portfolio values to 0

        Returns:
            pd.Series: Series of portfolio values normalized to 1
        """
        return self.normalize1() - 1


def backtest(cash,
             data,
             start,
             end,
             order_generator,
             slippage=0.0,
             commission=0,
             portfolio=Portfolio()):
    """ Backtesting function for Prophet
    """
    portfolio_shares = defaultdict(lambda: 0)
    portfolio_values = []
    prices = data.get('prices')
    if prices is None:
        raise ProphetException("Price data is required to run a backtest. "
                               "Please add a data generator with the name "
                               "property set to 'price'.")

    timestamps = prices.index.to_series().loc[start:]

    # Check if the last day doesn't have data yet
    # Like if it was early in the morning
    if not timestamps[-1] in prices:
        timestamps = timestamps[:-1]

    for timestamp in timestamps:
        orders = order_generator.run(data=data,
                                     timestamp=timestamp,
                                     prices=prices,
                                     cash=cash,
                                     portfolio=portfolio)

        for order in orders:
            # Get the price after slippage
            price = prices[order.symbol].loc[timestamp]
            if order.shares < 0:
                adjusted_price = price * (1 - slippage)
            else:
                adjusted_price = price * (1 + slippage)

            cash -= order.shares * adjusted_price
            cash -= commission
            portfolio_shares[order.symbol] += order.shares

        # Calculate total portfolio value for current timestamp
        current_value = cash
        portfolio_value = [prices[symbol].loc[timestamp] * shares for
                           symbol, shares in iteritems(portfolio_shares)]
        current_value += sum(portfolio_value)
        portfolio_values.append(current_value)

    return BackTest(dict(zip(timestamps, portfolio_values)),
                    index=timestamps)
