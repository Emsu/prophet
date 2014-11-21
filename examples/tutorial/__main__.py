import datetime as dt

from prophet import Prophet
from prophet.data import YahooCloseData
from prophet.analyze import default_analyzers

from bollinger import BollingerData
from eventstudy import BollingerEventStudy
from eventstudy import OrderGenerator


# Based on Homework #7 for Computational Investing
# http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
# Here we use 2 symbols and a benchmark to reduce data pulled
# but you can use the full sp5002012.txt file from QSTK
# You will have to adjust the portfolio analyzers
# The homework solution's analyzers start the analysis
# when the first trade is conducted instead of the entire
# duration of the backtest.
prophet = Prophet()
symbols = ["AAPL", "XOM", "SPX"]
prophet.set_universe(symbols)

prophet.register_data_generators(YahooCloseData(),
                                 BollingerData(),
                                 BollingerEventStudy())
prophet.set_order_generator(OrderGenerator())
backtest = prophet.run_backtest(start=dt.datetime(2008, 1, 1),
                                end=dt.datetime(2009, 12, 31), lookback=20)

prophet.register_portfolio_analyzers(default_analyzers)
analysis = prophet.analyze_backtest(backtest)
print analysis
# +----------------------------------------+
# | sharpe            |    -0.851247401074 |
# | average_return    | -2.04368321273e-07 |
# | cumulative_return |          -0.000103 |
# | volatility        |  3.81116761073e-06 |
# +----------------------------------------+


# Generate orders for your to execute today
# Using Nov, 10 2014 as the date because there might be no data for today's
# date (Market might not be open) and we don't want a examples to fail.
today = dt.datetime(2009, 12, 31)
print prophet.generate_orders(today, lookback=20)
