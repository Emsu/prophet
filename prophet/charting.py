import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def visualize_backtest(backtest):
    ''' visualize Portfolio Value (PV) over the backtest period '''
    pvNormed = backtest.normalize1()
    rollingMax = np.maximum.accumulate(backtest.values)
    pvDrawdown = (rollingMax - backtest.values) / rollingMax
    
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=False,
                             gridspec_kw={"height_ratios": [2, 1, 1]},
                             figsize=(9, 7))
    
    axPV, axDrawdown, axNormed = axes
    
    axPV.plot(backtest.index, backtest.values, color="blue")
    axPV.set_yticklabels(["{:,}".format(int(x)) for x in axPV.get_yticks().tolist()])
    axPV.set_title("Portfolio Value", size=12)
    
    #--------------------------------------------------------------------------------
    # annotate axPV with order details if there are any
    if backtest.ordersDict is not None:
        ordersDict = backtest.ordersDict
        for timestamp in ordersDict.keys():
            orders = ordersDict[timestamp]
            for order in orders:
                symbol, shares, tstamp = order.symbol, order.shares, timestamp.to_pydatetime()
                direction = "B" if shares > 0 else "S"
                desc = "%s %d %s" % (direction, shares, symbol)
                color = "g" if direction == "B" else "r"
                axPV.plot(tstamp, backtest.loc[tstamp], "^", markersize=5, color=color)
    #--------------------------------------------------------------------------------
    
    axDrawdown.plot(backtest.index, pvDrawdown, color="red")
    axDrawdown.set_yticklabels(["{:3.0f}%".format(x*100) for x in axDrawdown.get_yticks().tolist()])
    axDrawdown.set_title("Drawdown", size=12)
    
    axNormed.plot(pvNormed.index, pvNormed.values, color="green")
    axNormed.set_yticklabels(["{:0.2f}".format(x) for x in axNormed.get_yticks().tolist()])
    axNormed.set_title("Normalized Portfolio Value", size=12)
    
    fig.tight_layout()
    
    #--------------------------------------------------------------------------------
    # now we chart the stock prices and trades (only where there is a trade for the stock)
    if backtest.prices is not None:
        prices = backtest.prices
        
        stocks = []
        for orders in ordersDict.values():
            for order in orders:
                stocks.append(order.symbol)
        uniqueStocks = np.unique(stocks)
        numStocks = len(uniqueStocks)

        if numStocks == 0: # we have no trades
            print("No trades were generated for this backtest")
        else:
            figStocks, axesStocks = plt.subplots(nrows=numStocks, ncols=1, 
                                                 figsize=(9, 5 * numStocks))
            # if there are multiple plots / rows then axes will be a list of Axes objects
            # otherwise axes will just be an Axes object
            # to keep things consistent I've made axes a list of Axes objects 
            # (even when numStocks = 1)
            if not isinstance(axesStocks, list):
                axesStocks = [axesStocks]
            
            for i in range(len(axesStocks)):
                ax, stock = axesStocks[i], uniqueStocks[i]
                ax.plot(prices.index, prices[stock].values, color="blue")
                ax.set_title("%s Trading" % stock, size=12)
                if backtest.ordersDict is not None:
                    ordersDict = backtest.ordersDict
                    for timestamp in ordersDict.keys():
                        orders = ordersDict[timestamp]
                        for order in orders:
                            if order.symbol == stock:
                                tstamp = timestamp.to_pydatetime()
                                direction = "B" if order.shares > 0 else "S"
                                color = "g" if direction == "B" else "r"
                                ax.plot(tstamp, prices[stock].loc[tstamp], "^", markersize=5, color=color)
                
            figStocks.tight_layout()
    
    plt.show()
        
        