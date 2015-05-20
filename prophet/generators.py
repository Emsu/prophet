from datetime import datetime
from prophet.data import PandasDataGenerator


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
