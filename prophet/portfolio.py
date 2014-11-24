from six import iteritems


class Portfolio(dict):
    """ Portfolio object where keys are stock symbols and
    values are share counts. You can pass thise into a backtest
    to start with an initial basket of stocks.

    Note:
        Subclasses dict in v0.1
    """

    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        shares = []
        for key, value in iteritems(self):
            shares.append("%s=%s" % (key, value))
        share_info = ", ".join(shares)
        return "Portfolio(%s)" % share_info
