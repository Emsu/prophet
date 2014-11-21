.. _quickstart:

Quickstart
==========

.. code-block:: python

    # Hello World!
    import datetime as dt
    from prophet import Prophet
    from prophet.data import YahooCloseData
    from prophet.analyze import default_analyzers
    from prophet.orders import Orders


    # A simple order generator that buys nothing
    class OrderGenerator(object):
        def run(self, prices, timestamp, cash, **kwargs):
            return Orders()


    prophet = Prophet()
    prophet.set_universe(["AAPL", "XOM"])
    prophet.register_data_generators(YahooCloseData())
    prophet.set_order_generator(OrderGenerator())
    prophet.register_portfolio_analyzers(default_analyzers())

    backtest = prophet.run_backtest(start=dt.datetime(2010, 1, 1))
    analysis = prophet.analyze_backtest(backtest)
