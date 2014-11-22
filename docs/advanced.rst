.. _advanced:

Advanced
========

Slippage & Commissions
----------------------
The run_backtest method on the :class:`Prophet` object contains a commission and slippage option for you to make the backtest more realistic. Slippage is how much of the price increases (when buying) or decreases (when selling) from the price data. Commission represents the fees you pay per trade.

Please open an issue if those parameters aren't sufficent for your needs. See the :ref:`api` for more details.
