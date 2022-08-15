from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        self.atr = bt.ind.ATR(period=5)
        #crossover = bt.ind.CrossOver(sma1, sma2)
        #self.signal_add(bt.SIGNAL_LONG, crossover)
    def next(self):
        self.atr_max= max(list(self.atr))
        print(self.atr_max)
        #print(self.atr [0])
          
cerebro = bt.Cerebro()
cerebro.broker.setcash(200000.0) # set the money
cerebro.addstrategy(SmaCross)
data = btfeeds.GenericCSVData(
    dataname='d:/backtrader/stock_data.csv',
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
#cerebro.plot(iplot=False)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#print(data)











