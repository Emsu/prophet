from datetime import datetime

from prophet import Prophet
from prophet.data import YahooCloseData
from prophet.analyze import default_analyzers
from prophet.orders import Orders


class OrderGenerator(object):

    def __init__(self):
        super(OrderGenerator, self).__init__()
        self._data = dict()

    def run(self, prices, timestamp, cash, **kwargs):
        symbol = "AAPL"
        orders = Orders()
        if (prices.loc[timestamp, symbol] * 100) < cash:
            orders.add_order(symbol, 100)

        return orders


prophet = Prophet()
prophet.set_universe(['AAPL', 'XOM'])

prophet.register_data_generators(YahooCloseData())
prophet.set_order_generator(OrderGenerator())
backtest = prophet.run_backtest(start=datetime(2010, 1, 1))

prophet.register_portfolio_analyzers(default_analyzers)
analysis = prophet.analyze_backtest(backtest)
print analysis
# +--------------------------------------+
# | sharpe            |    1.09754359611 |
# | average_return    | 0.00105478425027 |
# | cumulative_return |         2.168833 |
# | volatility        |  0.0152560508189 |
# +--------------------------------------+

# Generate orders for you to execute today
# Using Nov, 10 2014 as the date because there might be no data for today's
# date (Market might not be open) and we don't want examples to fail.
today = datetime(2014, 11, 10)
print prophet.generate_orders(today)
# Orders[Order(symbol='AAPL', shares=100)]
