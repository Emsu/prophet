.. _tutorial:

Tutorial
==========

Introduction
------------

In this tutorial we will:

1. Implement Bollinger bands as an indicator using a 20 day look back. The upper band should represent the mean plus two standard deviation and here the lower band is the mean minus two standard deviation. We will issue "buy" orders when the following conditions are met:
    - Today's moving average breaks below the upper band.
    - Yesterday's moving average was above the lower band.
    - The market's moving average was 1.2 standard devations above the average.

.. note:: To learn more about what a bollinger band is, please see `this <http://www.investopedia.com/articles/technical/102201.asp>`_ article.

2. Create an event analyzer that will output a series of trades based on events. For simplicity, we will put a 1 for each timestamp and stock symbol pair where we want to execute a "buy" order.

3. Feed that data into the simulator and write an order generator that will create "buy" orders in blocks of 100 shares for each signal in the event study from step 2. The order generator will automatically sell the shares either 5 trading days later or on the last day of the simulation.

4. Print the performance of the strategy in terms of total return, average daily return, standard deviation of daily return, and Sharpe Ratio for the time period.

You can get the full source code of the tutorial `here <https://github.com/Emsu/prophet/tree/master/examples/tutorial>`_

The tutorial is based off of the last homework in QSTK. Since the portfolio is analyzed from the start date, the returned metrics will be different even if you use the same stock universe as the homework.

Data Generation
---------------

First you need to initialize the object and setup the stock universe:

.. code-block:: python

   prophet = Prophet()
   prophet.set_universe(["AAPL", "XOM"])

Then you register any data generators.

.. code-block:: python

   # Registering data generators
   prophet.register_data_generators(YahooCloseData(),
                                    BollingerData(),
                                    BollingerEventStudy())

.. note:: Please see the source code of :code:`prophet.data` for an example of a data generator. Data generators don't have to just pull raw data though like :class:`prophet.data.YahooCloseData` does. For instance, you can generate correlation data based off the price data. Prophet encourages you to logically separate out different steps in your analysis.

The :attr:`name` attribute of each of the generators is the key on the :attr:`data` object at which the generated data is stored. This data object is passed into each of the data generators. For example, since the :class:`YahooCloseData` object has the name "prices", we can use the price data in the :class:`BollingerData` that we execute right after.

.. code-block:: python

    import pandas as pd
    from prophet.data import DataGenerator


    class BollingerData(DataGenerator):
        name = "bollinger"

        def run(self, data, symbols, lookback, **kwargs):
            prices = data['prices'].copy()

            rolling_std = pd.rolling_std(prices, lookback)
            rolling_mean = pd.rolling_mean(prices, lookback)

            bollinger_values = (prices - rolling_mean) / (rolling_std)

            for s_key in symbols:
                prices[s_key] = prices[s_key].fillna(method='ffill')
                prices[s_key] = prices[s_key].fillna(method='bfill')
                prices[s_key] = prices[s_key].fillna(1.0)

            return bollinger_values

See how the :meth:`BollingerData.run` method uses the price data to generate a rolling standard deviation and rolling mean. The fillna method is used here to fill in missing data. Realistically, only the :meth:`bfill` method is uses in this example because the first 20 days won't have 20 prior days of price data to generate the rolling mean and standard deviation.

.. note:: :code:`prices` is also passed into the run function of all :code:`DataGenerator` objects for convenience but we want to emphasize that the :code:`data` object is where most data from data generators is stored.

The line below normalizes the bollinger data relative to the the rolling standard devation. This gives us the number of standard devations as an integer value. This means a value of 2 would be the upper band and a value of -2 would be the lower band.

.. code-block:: python

    bollinger_values = (prices - rolling_mean) / (rolling_std)

At this point we need one more generator. We will call this one BollingerEventStudy. Essentially, all it will do is run through the bollinger data and see if our conditions to issue a buy order are met.

.. code-block:: python

    class BollingerEventStudy(DataGenerator):
        name = "events"

        def run(self, data, symbols, start, end, lookback, **kwargs):
            bollinger_data = data['bollinger']

            # Add an extra timestamp before close_data.index to be able
            # to retrieve the prior day's data for the first day
            start_index = bollinger_data.index.get_loc(start) - 1
            timestamps = bollinger_data.index[start_index:]

            # Find events that occur when the market is up more then 2%
            bollinger_spy = bollinger_data['SPX'] >= 1.2  # Series
            bollinger_today = bollinger_data.loc[timestamps[1:]] <= -2.0
            bollinger_yesterday = bollinger_data.loc[timestamps[:-1]] >= -2.0
            # When we look up a date in bollinger_yesterday,
            # we want the data from the day before our input
            bollinger_yesterday.index = bollinger_today.index
            events = (bollinger_today & bollinger_yesterday).mul(
                bollinger_spy, axis=0)

            return events.fillna(0)

.. note:: Notice how all the data generators use the `pandas` library as much as possible instead of python for loops. This is key to keeping your simulations fast. In general, try to keep as much code as possible running in C using libraries like `numpy` and `pandas`.

Order Generation
----------------

Now we need to create an order generator. One thing we need to do is keep track of sell orders which we want to execute 5 days after the "buy" order. To do that, when we call run the first time, we run the :meth:`setup` method.

.. code-block:: python

    class OrderGenerator(object):

        def setup(self, events):
            sell_orders = pd.DataFrame(index=events.index, columns=events.columns)
            sell_orders = sell_orders.fillna(0)
            self.sell_orders = sell_orders

        def run(self, prices, timestamp, cash, data, **kwargs):
            """ Takes bollinger event data and generates orders """
            events = data['events']
            if not hasattr(self, 'sell_orders'):
                self.setup(events)

.. note:: The order generator API may change slightly in future version to allow for less hacky setup functions.

The rest of the :meth:`run` function will find all buy signals from the event study, find all sell orders from the sell orders Dataframe, and create orders from both sources. When creating an buy order, it will also add a sell order to the :attr:`sell_orders` Dataframe.

.. code-block:: python 

        # def run(...):
        #   ...

            orders = Orders()
            # Find buy events for this timestamp
            timestamps = prices.index
            daily_data = events.loc[timestamp]
            order_series = daily_data[daily_data > 0]
            # Sell 5 market days after bought
            index = timestamps.get_loc(timestamp)
            if index + 5 >= len(timestamps):
                sell_datetime = timestamps[-1]
            else:
                sell_datetime = timestamps[index + 5]

            symbols = order_series.index
            self.sell_orders.loc[sell_datetime, symbols] -= 100
            daily_sell_data = self.sell_orders.loc[timestamp]
            daily_sell_orders = daily_sell_data[daily_sell_data != 0]

            # Buy and sell in increments of 100
            for symbol in daily_sell_orders.index:
                orders.add_order(symbol, -100)

            daily_event_data = events.loc[timestamp]
            daily_buy_orders = daily_event_data[daily_event_data != 0]

            # Buy and sell in increments of 100
            for symbol in daily_buy_orders.index:
                orders.add_order(symbol, 100)

            return orders

Now we register the order generator and execute the backtest.

.. code-block:: python

    prophet.set_order_generator(OrderGenerator())
    backtest = prophet.run_backtest(start=dt.datetime(2008, 1, 1),
                                    end=dt.datetime(2009, 12, 31), lookback=20)

Portfolio Analysis
------------------

The last step is to analyze the portfolio:

.. code-block:: python

    prophet.register_portfolio_analyzers(default_analyzers)
    analysis = prophet.analyze_backtest(backtest)
    print(analysis)

:code:`default_analyzers` is a list of the four types of analysis we want. Much like the BollingerData generator, the Sharpe ratio analyzer uses the data returned by the volatility and average return analyzers to generate a Sharpe ratio.
