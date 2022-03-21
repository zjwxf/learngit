from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
data = btfeeds.GenericCSVData(
    dataname='stock_data.csv',
    fromdate=datetime(2011, 1, 1),
    todate=datetime(2012, 12, 31),
    nullvalue=0.0,
    dtformat=('%Y%m%d'),
    datetime=1,
    open=2,
    high=3,
    low=4,    
    close=5,
    volume=9,
    openinterest=-1
)
cerebro.adddata(data)
cerebro.run()
cerebro.plot(iplot=False)
















