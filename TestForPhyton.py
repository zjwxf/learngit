from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import tushare as ts
import pandas as pd
import matplotlib as plt
#import pyfolio as pf
#from IPython.display import (display, display_html, display_png, display_svg)
#import matplotlib.pyplot as plt
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = ts.pro_bar(ts_code='399673.SZ' ,asset='I',start_date ='20100101', end_date='20221025').iloc[::-1]
#df = ts.pro_bar(ts_code='159949.SZ' ,asset='FD',start_date ='20100101', end_date='20221022',).iloc[::-1]
df.trade_date= pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
data = btfeeds.PandasData( dataname=df, datetime='trade_date', open='open', high='high',low='low',    close='close',volume='vol',openinterest=-1)
class Ma_diff_strategy(bt.Strategy):
    #params = (('period1', 5),('period2',100)) #元组表达式
    #params= dict(period1=5, period2=100,) #字典表达式
    params = (('period1',5),('period2',100), ('period3',20), ('printlog', False), )  
    lines = ('sma5','sma100','ma_diff_pct','data_ma_diff',  'buy_sig','sell_sig',)
    def __init__(self):
        self.sma5= btind.SMA(self.data, period=self.params.period1)
        self.sma100= btind.SMA (self.data, period=self.p.period2)
        self.sma20 =btind.SMA(self.data,period=self.p.period3)
        #self.ema100 =btind.EMA(self.data, period=self.p.period2)
        #self.ema5 =btind.EMA(self.data, period=self.p.period1)
        self.data_ma_diff = self.sma5 -self.sma100
        self.ma_diff_pct = self.data_ma_diff/self.sma100    
        self.buy_sig = bt.And(self.ma_diff_pct <= -0.2,)      # 设置进场偏离
        self.sell_sig = bt.And( self.ma_diff_pct >= 0.03, )    # 设置获利偏离
        self.dataclose =self.datas[0].close
        #keep tracking of pending orders
        self.order = None

    def log(self,txt,dt=None):
        #logging function for this strategy
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

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
        #self.log('close,%2f.' % self.dataclose[0])
        #If a order is pending can not send a 2nd one
        #print(self.ma_diff_pct[0])
        #print(self.data_ma_diff[0])
        #print(self.sma5[0])
        if self.order:
            return
        #Check if we are in the market
        if not self.position:
            #0<-1<-2 close price go down for sequentially for 3 days
            if self.buy_sig :
                #if self.ma_diff_pct[0]< self.ma_diff_pct[-1] and self.ma_diff_pct[-1]<self.ma_diff_pct[-2]:
                #if self.data_ma_diff[0] < self.data_ma_diff[-1]:
                    #self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order =self.buy() #buy for which price?
        if self.position:
                #if len(self) >= (self.bar_executed + 5):
                     if self.sell_sig:
                        #if self. ma_diff_pct[0] > self.ma_diff_pct[-1]:
                            #self.log('Sell CREATE, %.2f' % self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                            self.order = self.sell()

"""        else:
            #if len(self) >= (self.bar_executed + 5):
                if self.sell_sig:
                    self.log('Sell CREATE, %.2f' % self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                    self.order = self.sell()"""

class PercentSizer(bt.Sizer):
    params = (
        ('percents', 10),
        ('retint', True),  #返回整数，而不是浮点数。
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            size = cash / data.close[0] * (self.params.percents / 100)
        else:
            size = position.size

        if self.p.retint:
            size = int(size)

        return size


if __name__ == '__main__':
    #Cereat a cerebro entity
    cerebro = bt.Cerebro()
    
    # data from tushare
    cerebro.adddata(data)
    cash=1000000
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.001)  #设置杠杆 不起作用 
    #cerebro.addsizer(bt.sizers.FixedSize,stake=100)  #固定，可以在stake= 调整
    cerebro.addsizer(bt.sizers.AllInSizerInt)
    #cerebro.addsizer(bt.sizers.PercentSizer)
    #cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # 应用于所有策略的缺省sizer
    cerebro.addobserver(bt.observers.DrawDown)
    #cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years,data=data, _name='datareturns')
    cerebro.addstrategy(Ma_diff_strategy)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    strat0 = results[0]
    #tret_analyzer = strat0.analyzers.getbyname('datareturns')
    #print(tret_analyzer.get_analysis())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    cerebro.plot()
   
"""
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    pf.create_simple_tear_sheet(returns,
                                positions=None,
                                transactions=None,
                                benchmark_rets=None,
                                slippage=None,
                                estimate_intraday='infer',
                                live_start_date= None,
                                turnover_denom='AGB',
                                header_rows=None)
    #print(pf.create_simple_tear_sheet(returns) ) # 与plt.show() 是一个方法，结果出一样的图    
    plt.show()
    print(results)"""

