from ctypes.wintypes import SIZE
import datetime  # For datetime objects
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import sys

class TestStrategy(bt.Strategy):
    params = ( ('exitbars', 20),) # parameter 'exitbars' is varliable 
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            return 
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price:%.2f, Cost:%.2f, Commmision %.2f, Size%.2f,ref:%.0f' %
                        (order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                        order.executed.size,
                        order.ref))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:#sell
                self.log('SELL EXECUTED, Price:%.2f, Cost:%.2f,commision:%.2f'%
                   (order.executed.price,
                    order.executed.value,
                    order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order =None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                (trade.pnl, trade.pnlcomm)
                )

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if self.dataclose[0]<self.dataclose[-1]:
                if self.dataclose[-1]<self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed +  self.params.exitbars):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                self.order = self.sell() 

if __name__=='__main__':
    cerebro =bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    data = bt.feeds.GenericCSVData(
        dataname= 'stock_data.csv',
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
#cerebro.plot(iplot=None)

