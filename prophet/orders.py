from collections import namedtuple


Order = namedtuple('Order', ['symbol', 'shares'])


class Orders(list):
    """ Orders object that an OrderGenerator should return. """

    def __init__(self, *args):
        super(Orders, self).__init__()
        self.extend(args)

    def add_order(self, symbol, shares):
        """ Add an order to the orders list.

        Parameters:
            symbol (str): Stock symbol to purchase
            shares (int): Number of shares to purchase. Can be negative.
        """
        self.append(Order(symbol, shares))

    def __repr__(self):
        return "Orders%s" % super(Orders, self).__repr__()
