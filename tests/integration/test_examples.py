from datetime import datetime
import os

from prophet import Prophet
from prophet.data import YahooCloseData
from prophet.analyze import default_analyzers
from prophet.orders import Order
from prophet.orders import Orders


CACHE_PATH = os.path.join(os.path.dirname(__file__), 'data')


class OrderGenerator(object):

    def run(self, prices, timestamp, cash, **kwargs):
        symbol = "AAPL"
        orders = Orders()
        if (prices.loc[timestamp, symbol] * 100) < cash:
            orders.add_order(symbol, 100)
        return orders


def test_quickstart():
    prophet = Prophet()
    prophet.set_universe(['AAPL', 'XOM'])

    print CACHE_PATH
    prophet.register_data_generators(YahooCloseData(cache_path=CACHE_PATH))
    prophet.set_order_generator(OrderGenerator())
    backtest = prophet.run_backtest(start=datetime(2010, 1, 1),
                                    end=datetime(2014, 11, 21))

    prophet.register_portfolio_analyzers(default_analyzers)
    analysis = prophet.analyze_backtest(backtest)
    assert round(analysis['sharpe'], 10) == 1.1083876014
    assert round(analysis['average_return'], 10) == 0.0010655311
    assert round(analysis['cumulative_return'], 10) == 2.2140809296
    assert round(analysis['volatility'], 10) == 0.0152607097

    today = datetime(2014, 11, 10)
    expected_orders = Orders(Order(symbol='AAPL', shares=100))
    assert prophet.generate_orders(today) == expected_orders
