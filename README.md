![prophet](docs/_static/img/logo.png?raw=true "Prophet")

> Prophet is a Python microframework for financial markets. Prophet strives to let the programmer focus on modeling financial strategies, portfolio management, and analyzing backtests. It achieves this by having few functions to learn to hit the ground running, yet being flexible enough to accomodate sophistication.

![build status](https://travis-ci.org/Emsu/prophet.svg?branch=master "Travis Build Status")

See the [documentation](http://prophet.michaelsu.io/) for more details.

Join the mailing list [here](https://groups.google.com/forum/#!forum/prophet-financial-framework) or join by [email](mailto:prophet-financial-framework+subscribe@googlegroups.com?subject=Subscribe).

## Quickstart

```python
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
```

## Contribute

Run the following to your development environment setup:

```bash
git clone git@github.com:Emsu/prophet.git
cd prophet
virtualenv env
pip install dev-requirements.txt
python setup.py develop
```

## Credits
Prophet wouldn't be possible without the wonderful [pandas](https://github.com/pydata/pandas) library and is inspired by [QSTK](https://github.com/tucker777/QSTK) and [Zipline](https://github.com/quantopian/zipline).

The [trading calendar util](https://github.com/Emsu/prophet/blob/master/prophet/utils/tradingcalendar.py) in Prophet is from [Zipline](https://github.com/quantopian/zipline) which is under the [Apache 2.0 License](https://github.com/quantopian/zipline/blob/master/LICENSE).
