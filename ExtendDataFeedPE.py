from datetime import datetime
from backtrader import Indicator
import backtrader as bt
import backtrader.indicators as btind


class MyStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self): #Any Indicator (or value thereof derived) declared during __init__ will be precalculated before next is called.

        self.sma1 = btind.SimpleMovingAverage(self.data)
        self.ema1 = btind.ExponentialMovingAverage()

        self.close_over_sma = self.data.close > self.sma1
        self.close_over_ema = self.data.close > self.ema1
        self.sma_ema_diff = self.sma1 - self.ema1

        self.buy_sig = bt.And(self.close_over_sma, self.close_over_ema, self.sma_ema_diff > 0)
        self.sell_sig =bt.And(self.data.close >self.data.close[0]*1.02 , self.buy_sig == True)
        print('okokokokokokoko')
        print(self.buy_sig)


    def next(self):
        #print('ok')
        #if self.buy_sig:    # buy_sig is not define？？？？？？？？
        if self.buy_sig:
            self.buy()
            self.log('BUY CREATE, %.2f' % self.data.close[0])
            print('indicator calculation is ok')
        if self.sell_sig:
            self.log('sell_sig == Ture')
            self.sell()
            self.log('SELL CREATE,%.2f' % self.data.close[0])
        #else:
            #print('no signal')
    
if __name__=='__main__':
    cerebro =bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    data = bt.feeds.GenericCSVData(
        dataname= 'stock_data.csv',
        fromdate=datetime(2011, 1, 1),
        todate=datetime(2011, 12, 31),
        nullvalue=0.0,
        dtformat=('%Y%m%d'),
        datetime=1,
        open=2,
        high=3,
        low=4,
        close=5,
        volume=9,
        openinterest=-1,
    )
cerebro.adddata(data)
#self.sizer.setsizing(self.params.stake)
cerebro.addsizer(bt.sizers.FixedSize,stake=4000)
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
print('Starting Protfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#cerebro.plot(iplot=None)"""
