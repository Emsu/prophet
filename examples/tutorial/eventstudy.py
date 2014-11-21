import pandas as pd
import datetime as dt

from prophet.orders import Orders
from prophet.data import DataGenerator


class BollingerEventStudy(DataGenerator):
    name = "events"

    def run(self, data, symbols, start, end, lookback, **kwargs):
        if not end:
            end = dt.datetime.now()

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
