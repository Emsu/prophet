#!/usr/bin/env python
from prophet.utils.formatters import dict_to_table

import math


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
        return ((avg_daily_returns - risk_free_rate) / volatility
                * math.sqrt(trading_days))


class AverageReturn(Analyzer):
    name = 'average_return'

    def run(self, backtest, **kwargs):
        return backtest.get_daily_returns().mean()


class CumulativeReturn(Analyzer):
    name = "cumulative_return"

    def run(self, backtest, **kwargs):
        return backtest.normalize0()[-1]


class Analysis(dict):

    def __repr__(self):
        """ Represents Analysis object as a text table. """
        return dict_to_table(self)


default_analyzers = [Volatility(), AverageReturn(),
                     Sharpe(), CumulativeReturn()]
