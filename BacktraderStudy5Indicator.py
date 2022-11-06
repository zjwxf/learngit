from ctypes.wintypes import SIZE
import backtrader.indicators as btind 
import datetime  # For datetime objects
from datetime import datetime #tushare 
import backtrader as bt
import backtrader.feeds as btfeeds
import sys
import backtrader.indicators
import tushare as ts
import pandas as pd

class TestStrategy(bt.Strategy):
    params = ( ('mpperiod', 60),) # parameter 'exitbars' is varliable 
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.mpperiod)
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
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                (trade.pnl, trade.pnlcomm)
                )

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if self.dataclose[0]>self.sma[0]:
                #if self.dataclose[-1]<self.dataclose[-2]:
                    #self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            if self.dataclose[0] >self.sma[0]:
                #len(self) >= (self.bar_executed +  self.params.exitbars)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                self.order = self.sell() 

if __name__=='__main__':
    cerebro =bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    df_stock_basic = pro.stock_basic()
    df = pro.daily(ts_code='000001.SZ', start_date='20210101', end_date='20220101').iloc[::-1]
    # 由于trade_date是字符串'20220202，BackTrader无法识别，转换为时间格式2022-02-02 00:00:00
    df.trade_date = pd.to_datetime(df.trade_date)
    data = btfeeds.PandasData(
        dataname=df,
        fromdate=datetime(2021, 1, 1),
        todate=datetime(2022, 1, 1),
        datetime='trade_date',
        open='open',
        high='high',
        low='low',
        close='close',
        volume='vol',
        openinterest=-1
    )

"""    data = bt.feeds.GenericCSVData(
        dataname= 'd:/backtrader/stock_data.csv',
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
    )"""
cerebro.adddata(data)
#self.sizer.setsizing(self.params.stake)
cerebro.addsizer(bt.sizers.FixedSize,stake=4000)
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
print('Starting Protfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(iplot=None)

