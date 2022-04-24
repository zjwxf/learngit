from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds


class Teststrategy(bt.Strategy):
    def log(self,txt,dt=None):
        #logging function for this strategy
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        #keep a reference to the "close" line in the data[0] dataseries
        self.dataclose =self.datas[0].close
        #keep tracking of pending orders
        self.order = None
    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            #Buy/Sell order submitted/accepted to/by broker-nothing to do
            return
            #Check if an order has been completed
            #Attention: broker could reject order if not ennough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %2f.' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %2f.' % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        #write down : no pending order
        self.order = None
    def next(self):
        #log the closing price of the series from the reference
        self.log('close,%2f.' % self.dataclose[0])
        #If a order is pending can not send a 2nd one
        if self.order:
            return
        #Check if we are in the market
        if not self.position:
            #0<-1<-2 close price go down for sequentially for 3 days
            if self.dataclose[0]<self.dataclose[-1]:
                if self.dataclose[-1]<self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order =self.buy() #buy for which price?
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, %.2f' %self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                self.order = self.sell() 
if __name__ == '__main__':
    #Cereat a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Teststrategy)
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
    cerebro.broker.setcash(100000.00)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
