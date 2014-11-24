from datetime import datetime
import os

import pandas as pd
from pandas.io import data as web
from prophet.exceptions import ProphetException
from prophet.utils import trading_days


class DataGenerator(object):

    def __init__(self, cache_path=None, data_path=None):
        # Caching based on Zipline
        self.DATA_PATH = data_path or os.path.join(
            os.path.expanduser("~"), '.prophet', 'data')
        self.CACHE_PATH = cache_path or os.path.join(
            os.path.expanduser("~"), '.prophet', 'cache')

    def get_data_start(self, start, lookback):
        start_index = trading_days.get_loc(start)
        return trading_days[start_index - lookback]

    def get_cache_filepath(self, name):
        if not os.path.exists(self.CACHE_PATH):
            os.makedirs(self.CACHE_PATH)
        return os.path.join(self.CACHE_PATH, name)

    def sanitize_name(self, name):
        return name.replace(os.path.sep, '--')


class PandasDataGenerator(DataGenerator):

    def run(self, data, start, end, symbols, source, lookback=0):
        data_start = self.get_data_start(start, lookback)

        # Current caching implementation based on Zipline
        symbols_data = dict()
        for symbol in symbols:
            symbol_path = self.sanitize_name(symbol)
            cache_filename = "{stock}-{start}-{end}.csv".format(
                stock=symbol_path, start=data_start, end=end
            ).replace(':', '-')
            cache_filepath = self.get_cache_filepath(cache_filename)
            if os.path.exists(cache_filepath):
                symbol_data = pd.DataFrame.from_csv(cache_filepath)
            else:
                symbol_data = web.DataReader(symbol, 'yahoo',
                                             data_start, end).sort_index()
                symbol_data.to_csv(cache_filepath)
            symbols_data[symbol] = symbol_data

        symbols_panel = pd.concat(symbols_data).to_panel()
        symbols_panel = symbols_panel.swapaxes('minor', 'major')
        if symbols_panel.empty:
            ProphetException("No data for the range specified:"
                             " %s to %s" % (data_start, end))

        symbols_panel = symbols_panel.fillna(method='ffill')
        symbols_panel = symbols_panel.fillna(method='bfill')
        symbols_panel = symbols_panel.fillna(1.0)
        return symbols_panel.loc[:, ((symbols_panel.major_axis >= data_start)
                                     & (symbols_panel.major_axis <= end))]


class YahooCloseData(PandasDataGenerator):
    name = 'prices'

    def run(self,
            data,
            symbols,
            start=datetime(2007, 1, 1),
            end=None,
            lookback=0):
        if not end:
            end = datetime.now()

        symbols_data = super(YahooCloseData, self).run(
            data=data, symbols=symbols, start=start,
            end=end, lookback=lookback, source="yahoo")

        return symbols_data['Adj Close']


class YahooVolumeData(PandasDataGenerator):
    name = 'volume'

    def run(self,
            data,
            symbols,
            start=datetime(2007, 1, 1),
            end=None,
            lookback=0):
        if not end:
            end = datetime.now()

        symbols_data = super(YahooVolumeData, self).run(
            data=data, symbols=symbols, start=start,
            end=end, lookback=lookback, source="yahoo")

        return symbols_data['Volume']
