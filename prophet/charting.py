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
    
    axDrawdown.plot(backtest.index, pvDrawdown, color="red")
    axDrawdown.set_yticklabels(["{:3.0f}%".format(x*100) for x in axDrawdown.get_yticks().tolist()])
    axDrawdown.set_title("Drawdown", size=12)
    
    axNormed.plot(pvNormed.index, pvNormed.values, color="green")
    axNormed.set_yticklabels(["{:0.2f}".format(x) for x in axNormed.get_yticks().tolist()])
    axNormed.set_title("Normalized Portfolio Value", size=12)
    
    fig.tight_layout()
    plt.show()