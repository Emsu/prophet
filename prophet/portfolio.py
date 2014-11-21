class Portfolio(dict):

    def __unicode__(self):
        return self.__repr__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        shares = []
        for key, value in self.iteritems():
            shares.append("%s=%s" % (key, value))
        share_info = ", ".join(shares)
        return "Portfolio(%s)" % share_info
