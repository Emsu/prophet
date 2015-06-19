from datetime import datetime
from prophet.data import PandasDataGenerator

class YahooData(PandasDataGenerator):

    def __init__(self, column, name):
        super(YahooData, self).__init__()
        self._column = column
        self.name = name

    def run(self,
            data,
            symbols,
            start=datetime(2007, 1, 1),
            end=None,
            lookback=0):
        if not end:
            end = datetime.now()

        symbols_data = super(YahooData, self).run(
            data=data, symbols=symbols, start=start,
            end=end, lookback=lookback, source="yahoo")

        return symbols_data[self._column]
