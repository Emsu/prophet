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
