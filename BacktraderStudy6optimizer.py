from datetime import datetime
import backtrader as bt
import sys
import os
import backtrader.feeds as btfeeds


class TestStrategy(bt.Strategy):
    params=(('maperiod',None),('printlog',False))
    def log(self,txt,dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime(0)
            print('%s, %s' %(dt.isoformat(),txt))
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma= bt.indicators.SimpleMovingAverage(self.datas[0],period=self.params.maperiod)
    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            return 
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED,ref:%.0f,Stock:%s Price:%.2f, Cost:%.2f, Commmision %.2f, Size%.2f,' %
                        (order.ref,
                        order.data._name,
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm,
                        order.executed.size,
                        ))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:#sell
                self.log('SELL EXECUTED, ref:%.0f, Stock:%s, Price:%.2f, Cost:%.2f,commision:%.2f,Size%.2f'%
                   (order.ref,
                   order.data._name,
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm,
                    order.executed.size
                    ))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order =None
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f,NET%.2f' %(trade:pnl, trade.pnlcomm))

    def next(self):
        self.log('close,%.2f' %self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if self.dataclose[0]>self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy() 
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %(self.params.maperiod,self.broker.getvalue(),doprint=True)"""
""""
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    strats = cerebro.optstrategy(TestStrategy,maperiod=range(10,31))
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
cerebro.addsizer(bt.sizers.FixedSize,stake=4000)
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
print('Starting Protfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run(maxcpus=1)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())"""


print("%04d" % 5)