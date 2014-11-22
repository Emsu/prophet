.. _api:

API
===

This part of the documentation covers all the interfaces of Prophet.
For parts where Flask depends on external libraries, we document the
most important right here and provide links to the canonical
documentation.


Prophet Object
--------------

.. module:: prophet

.. autoclass:: Prophet
   :members:

Order Objects
-------------

.. module:: prophet.orders

.. autoclass:: Order

.. autoclass:: Orders
   :members:

Backtest Object
---------------

.. module:: prophet.backtest

.. autoclass:: BackTest
   :members:

Portfolio Objects
-----------------

.. module:: prophet.portfolio

.. autoclass:: Portfolio
   :members:

Analyzer Objects
-----------------

.. module:: prophet.analyze

.. autoclass:: Analyzer
   :members:

.. autoclass:: Volatility
   :members:

.. autoclass:: AverageReturn
   :members:

.. autoclass:: Sharpe
   :members:

.. autoclass:: CumulativeReturn
   :members:

.. autodata:: default_analyzers

Data Objects
------------

.. module:: prophet.data

.. autoclass:: DataGenerator
   :members:

.. autoclass:: PandasDataGenerator
   :members:

.. autoclass:: YahooCloseData
   :members:

.. autoclass:: YahooVolumeData
   :members:
