import datetime as dt

from prophet.analyze import Analysis
from prophet.portfolio import Portfolio
from prophet.backtest import backtest
from prophet.exceptions import ProphetException
from prophet.utils import trading_days


class Prophet(object):
    """ The application object. Serves as the primary interface for using the
    Prophet library.

    Attributes:
        config (dict): Dictionary of settings to make available to other
            functions. Useful for things like ``RISK_FREE_RATE``.
    """

    def __init__(self):
        self.config = dict()
        self._data_generators = []
        self._backtest_analyzers = []
        self._symbols = []
        self._order_generator = None
        super(Prophet, self).__init__()

    def run_backtest(self,
                     start,
                     end=None,
                     lookback=0,
                     slippage=0.0,
                     commission=0.0,
                     cash=1000000,  # $1,000,000
                     initial_portfolio=Portfolio(),
                     ):
        """ Runs a backtest over a given time period.

        Args:
            start (datetime): The start of the backtest window
            end (datetime): The end of the backtest windows
            lookback (int): Number of trading days you want data for
                before the start date
            slippage (float): Percent price slippage when executing order
            commission (float): Amount of commission paid per order
            cash (int): Amount of starting cash
            portfolio (prophet.portfolio.Portfolio): Starting portfolio

        Return:
            pandas.backtest.BackTest
        """
        # Setup
        if not end:
            today = dt.date.today()
            end = dt.datetime.combine(today, dt.time())

        if not self._order_generator:
            raise ProphetException("Must set an order generator by calling"
                                   "set_order_generator.")

        timestamps = trading_days[(trading_days >= start) &
                                  (trading_days <= end)]
        effective_start = timestamps[0]

        data = self._generate_data(start=effective_start,
                                   end=end,
                                   lookback=lookback)

        # Run backtest
        return backtest(cash=cash,
                        data=data,
                        start=effective_start,
                        end=end,
                        slippage=slippage,
                        commission=commission,
                        portfolio=initial_portfolio,
                        order_generator=self._order_generator,
                        )

    def _generate_data(self, start, end, lookback=0):
        # Generate data
        data = dict()
        for generator in self._data_generators:
            data[generator.name] = generator.run(data,
                                                 end=end,
                                                 start=start,
                                                 lookback=lookback,
                                                 symbols=self._symbols)
        return data

    def set_universe(self, symbols):
        """ Sets the list of all tickers symbols that will be used.

        Args:
            symbols (list of str): Ticker symbols to be used by Prophet.
        """
        self._symbols = symbols

    def register_data_generators(self, *functions):
        """ Registers functions that generate data to be assessed in
        the order generator.

        Args:
            functions (list): List of functions.
        """
        self._data_generators.extend(functions)

    def set_order_generator(self, order_generator):
        """ Sets the order generator for backtests.

        Args:
            order_generator: Instance of class with a run method that generates
            prophet.orders.Orders
        """
        self._order_generator = order_generator

    def register_portfolio_analyzers(self, functions):
        """ Registers a list of functions that are sequentially executed to
        generate data. This list is appended to list of existing data
        generators.

        Args:
            functions (list of function): Each function in the list of args is
                executed in sequential order.
        """
        self._backtest_analyzers.extend(functions)

    def analyze_backtest(self, backtest):
        """ Analyzes a backtest with the registered portfolio analyzers.

        Args:
            backtest (prophet.backtest.BackTest): a backtest object

        Return:
            prophet.backtest.BackTest
        """
        data = Analysis()
        for analyzer in self._backtest_analyzers:
            data[analyzer.name] = analyzer.run(backtest=backtest,
                                               config=self.config,
                                               data=data)
        return data

    def generate_orders(self,
                        target_datetime,
                        lookback=0,
                        cash=1000000,
                        buffer_days=0,
                        portfolio=Portfolio()):
        """ Generates orders for a given day. Useful for generating trade
        orders for a your personal account.

        Args:
            target_datetime (datetime): The datetime you want to
                generate orders for.
            lookback (int): Number of trading days you want data for before the
                (target_datetime - buffer_days)
            cash (int): Amount of starting cash
            buffer_days (int): number of trading days you want extra data
                generated for. Acts as a data start date.
            portfolio (prophet.portfolio.Portfolio): Starting portfolio
        """
        target_datetime_index = trading_days.get_loc(target_datetime)
        start = trading_days[target_datetime_index - buffer_days]
        data = self._generate_data(start,
                                   target_datetime,
                                   lookback)
        prices = data.get('prices')
        if prices is None:
            raise ProphetException("Price data is required to run a backtest. "
                                   "Please add a data generator with the name "
                                   "property set to 'price'.")
        return self._order_generator.run(prices=prices,
                                         data=data,
                                         timestamp=target_datetime,
                                         cash=cash,
                                         portfolio=portfolio)
