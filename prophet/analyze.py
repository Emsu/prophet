from prophet.utils.formatters import dict_to_table

import math
import numpy as np


class Analyzer(object):
    def __repr__(self):
        return self.name


class Volatility(Analyzer):
    name = 'volatility'

    def run(self, backtest, **kwargs):
        return backtest.get_daily_returns().std()


class Sharpe(Analyzer):
    name = 'sharpe'

    def run(self, data, config, **kwargs):
        avg_daily_returns = data['average_return']
        volatility = data['volatility']
        risk_free_rate = config.get('RISK_FREE_RATE', 0)
        trading_days = config.get('YEARLY_TRADING_DAYS', 252)
        if volatility == 0:
            return 0
        return ((avg_daily_returns - risk_free_rate) / volatility
                * math.sqrt(trading_days))

class Sortino(Analyzer):
    name = 'sortino'

    def run(self, backtest, data, config, **kwargs):
        avg_daily_returns = data['average_return']
        negative_returns = backtest.get_daily_returns()[backtest.get_daily_returns() < 0]
        volatility_negative_returns = negative_returns.std()
        risk_free_rate = config.get('RISK_FREE_RATE', 0)
        trading_days = config.get('YEARLY_TRADING_DAYS', 252)
        if volatility_negative_returns == 0:
            return 0
        return ((avg_daily_returns - risk_free_rate) / volatility_negative_returns
                * math.sqrt(trading_days))

class AverageReturn(Analyzer):
    name = 'average_return'

    def run(self, backtest, **kwargs):
        return backtest.get_daily_returns().mean()


class CumulativeReturn(Analyzer):
    name = "cumulative_return"

    def run(self, backtest, **kwargs):
        return backtest.normalize0()[-1]


class MaximumDrawdown(Analyzer):
    name = "maximum_drawdown"

    def run(self, backtest, **kwargs):
        dd_end = np.argmax(np.maximum.accumulate(backtest) - backtest)
        dd_start = np.argmax(backtest[:dd_end])
        if backtest[dd_start] == 0:
            return 0
        return 1-backtest[dd_end]/backtest[dd_start]


class Analysis(dict):

    def __repr__(self):
        """ Represents Analysis object as a text table. """
        return dict_to_table(self)


default_analyzers = [Volatility(), AverageReturn(),
                     Sharpe(), CumulativeReturn(), MaximumDrawdown(), Sortino()]
