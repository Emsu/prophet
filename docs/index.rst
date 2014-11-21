.. Prophet documentation master file, created by
   sphinx-quickstart on Wed Nov 19 05:52:00 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Prophet
==================

Prophet is a microframework for financial markets. Prophet strives to let the programmer focus on modeling financial strategies, portfolio management, and analyzing backtests. It achieves this by having few functions to learn to hit the ground running, yet being flexible enough to accomodate sophistication.


.. code-block:: python

    # Hello World!

    from prophet import Prophet

    def generate_orders():
        pass
   
    symbols = ['GOOG']

    prophet = Prophet()
    prophet.set_universe(symbols)
    prophet.set_order_generator(generate_orders)
    backtest = prophet.run_backtest()
    print prophet.analyze_backtest(backtest)

See the :ref:`tutorial` for a more thorough introduction.

Features
--------

- Flexible market backtester
- Convenient order generator
- See :ref:`roadmap` for upcoming features


User Guide
----------

.. toctree::
   :maxdepth: 2

   tutorial
   advanced
   best_practices


API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


Contributor Guide
-----------------


Additional Notes
----------------

.. toctree::
   :maxdepth: 1

   roadmap
   changelog
   license
