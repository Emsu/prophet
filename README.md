prophet
=======

Python lightweight financial markets framework for programmers

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

## Design Goals

### API surface:
The high level API of prophet will be small (but powerful) so that it will be easy to pickup and use.

### Flexible
Despite the small surface of the high level API, prophet provides the building blocks by exposing low level functions you can use to create custom version of the high level API if you need it.
