prophet
=======

> Prophet is a Python microframework for financial markets. Prophet strives to let the programmer focus on modeling financial strategies, portfolio management, and analyzing backtests. It achieves this by having few functions to learn to hit the ground running, yet being flexible enough to accomodate sophistication.

## Quickstart

Backtesting

Trading

    current_portfolio = Portfolio()
    prophet.generate_orders()

# Custom Data Source

If you want to use a custom data source for stock prices, write a function that loads the data
and pass it into register_data_analyzers using the 'prices' keyword.

    prophet.register_data_generators(bollinger, find_events, prices=custom_data_func)

You can also just add it to the list of data generators if you still want the default price data

    # custom_forex_data_func = some_function
    prophet.register_data_generators(custom_forex_data_func, bollinger, find_events)

Please feel free to contribute your data source function so others can use it too.

## Contribute

Please ensure that the tests pass before you open a pull request.

    pip install dev-requirements.txt

## Credits
Prophet wouldn't be possible without the wonderful [pandas](https://github.com/pydata/pandas) library and is inspired by [QSTK](https://github.com/tucker777/QSTK) and [Zipline](https://github.com/quantopian/zipline).
The [trading calendar util](https://) in Prophet is from [Zipline](https://github.com/quantopian/zipline) which is under the [Apache 2.0 License](https://github.com/quantopian/zipline/blob/master/LICENSE).
