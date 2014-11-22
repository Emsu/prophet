.. _tutorial:

Tutorial
==========

Introduction
------------

You can get the full source code of the tutorial `here <https://github.com/Emsu/prophet/tree/master/examples/tutorial>`_

The tutorial is based off of the last homework in QSTK. There are some differences that will be explained. This tutorial is currently unfinished so please read the source code linked above. Hopefully I'll get it done tomorrow.

Data Generation
---------------

First you need to initialize the object and setup the stock universe:

.. code-block:: python

   prophet = Prophet()
   prophet.set_universe(["AAPL", "XOM"])

Then you register any data generators. Please see the source code of prophet.data for an example of a data generator. Data generators don't have to just pull raw data though like prophet.data.YahooCloseData does. For instace, you can generate correlation data based off the price data. Prophet encourages you to 

.. code-block:: python

   # Registering data generators
   prophet.register_data_generators(YahooCloseData())
   prophet.set_order_generator(OrderGenerator())
   prophet.register_portfolio_analyzers(default_analyzers)

Order Generation
----------------

Portfolio Analysis
------------------
