from collections import namedtuple


Order = namedtuple('Order', ['symbol', 'shares'])


class Orders(list):

    def add_order(self, symbol, shares):
        self.append(Order(symbol, shares))

    def __repr__(self):
        return "Orders%s" % super(Orders, self).__repr__()
