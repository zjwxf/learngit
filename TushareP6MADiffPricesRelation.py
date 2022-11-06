from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import tushare as ts

from dataclasses import dataclass
import os
from re import S
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime 
import threading
import pandas as pd
import numpy as np
import requests
import tushare as ts


class Ma_diff_strategy(bt.Strategy):
    params = (('period5', 5),('period100',100))
    lines = ('sma5','sma100')

    def __init__(self):

        sma5= btind.SimpleMovingAverage(self.data, period=self.params.period5)
        sma100= btind.SMA (self.data, period=self.p.period100)

        sma1 = btind.SimpleMovingAverage(self.data)
        ema1 = btind.ExponentialMovingAverage()

        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1

        buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)

        #self.sma5 = bt.indicators.SMA(self.data, period=self.p.period5)
        #self.sma100 = bt.indicators.SMA(self.data, period=self.p.period100)

        #sma5 = btind.SimpleMovingAverage(self.data,period=self.p.period5)
        #sma100 = btind.SimpleMovingAverage(self.data.period=self.p.period100)
    
        #close_over_sma = self.data.close > sma1
        #close_over_ema = self.data.close > ema
        data_ma_diff = self.sma5[0] -self.sma100[0]
        ma_diff_pct = self.data_ma_diff[0]/self.sma100[0]

        buy_sig = bt.And(self.ma_diff_pct[0] <= -10, self.sma5[0]<self.sma5[-1])
   
    """def next(self):
        if buy_sig:
            self.buy() 
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
            if self.ma-diff[0] <= -10:
                if self.data_ma_diff[-1]<self.data_ma_diff[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order =self.buy() #buy for which price?
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATE, %.2f' %self.dataclose[0])
                #keep track of the created order to avoid 2nd order
                self.order = self.sell() """
if __name__ == '__main__':
    #Cereat a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Ma_diff_strategy)
    # data from tushare
    pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    df = ts.pro_bar(ts_code='399006.SZ',asset='I' ,start_date ='2019101', end_date='20210101').iloc[::-1]
    df.trade_date=pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
    data = btfeeds.PandasData(
        dataname=df,
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2021, 1, 1),
        datetime='trade_date',
        open='open',
        high='high',
        low='low',    
        close='close',
        volume='vol',
        openinterest=-1
    )
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.00)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    #print(ma_diff_pct)


"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import tushare as ts
import pandas as pd
from IPython.display import (display, display_html, display_png, display_svg)
import matplotlib.pyplot as plt
import numpy as np

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=25)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
#从tushare 引入数据
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = pro.daily(ts_code='002020.SZ', start_date='2019101', end_date='20210101').iloc[::-1]
df.trade_date=pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
data = btfeeds.PandasData(
    dataname=df,
    fromdate=datetime(2019, 1, 1),
    todate=datetime(2021, 1, 1),
    datetime='trade_date',
    open='open',
    high='high',
    low='low',    
    close='close',
    volume='vol',
    openinterest=-1
)
print(df.head())
print(data)"""
"""cerebro.adddata(data)
# 设置投资金额100000.0
cerebro.broker.setcash(10000.0)
cerebro.addsizer(bt.sizers.FixedSize,stake=500)
cerebro.broker.setcommission(commission=0.001)
# 引擎运行前打印期出资金
print('组合期初资金: %.2f' % cerebro.broker.getvalue())
cerebro.run()
# 引擎运行后打期末资金
print('组合期末资金: %.2f' % cerebro.broker.getvalue())
#cerebro.plot(iplot=False)

#cerebro  addanalyzer 加入 bt.analyzer.Pyfolio
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')   
results = cerebro.run()
strat = results[0]
pyfoliozer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
#print(returns.head())
#print(gross_lev)
# pyfolio showtime
import pyfolio as pf
#pf.create_full_tear_sheet(returns)
#live_start_date ='2019-01-01'
#pf.create_returns_tear_sheet(returns)
pf.create_simple_tear_sheet(returns,
                             positions=None,
                             transactions=None,
                             benchmark_rets=None,
                             slippage=None,
                             estimate_intraday='infer',
                             live_start_date= None,
                             turnover_denom='AGB',
                             header_rows=None)
print(pf.create_simple_tear_sheet(returns) )# 与plt.show() 是一个方法，结果出一样的图    
plt.show()
"""
"""
pf.create_perf_attrib_tear_sheet(returns,
                                  positions,
                                  factor_returns= benchmark_rets,  
                                  factor_loadings=None,
                                  transactions=None,
                                  pos_in_dollars=True,
                                  #factor_partitions=FACTOR_PARTITIONS,
                                  return_fig=False)
report=pf.create_perf_attrib_tear_sheet(returns)
print(report.head())
plt.show()"""


"""pf.create_full_tear_sheet(returns,
                           positions=None,
                           transactions=None,
                           market_data=None,
                           benchmark_rets=None,
                           slippage=None,
                           live_start_date=None,
                           sector_mappings=None,
                           round_trips=False,
                           estimate_intraday='infer',
                           hide_positions=False,
                           cone_std=(1.0, 1.5, 2.0),
                           bootstrap=False,
                           unadjusted_returns=None,
                           turnover_denom='AGB',
                           set_context=True,
                           factor_returns=None,
                           factor_loadings=None,
                           pos_in_dollars=True,
                           header_rows=None,
                           )
plt.show()"""


"""FACTOR_PARTITIONS = {

    
    'style': ['momentum', 'size', 'value', 'reversal_short_term',
              'volatility'],
    'sector': ['basic_materials', 'consumer_cyclical', 'financial_services',
               'real_estate', 'consumer_defensive', 'health_care',
               'utilities', 'communication_services', 'energy', 'industrials',
               'technology']
}
pf.create_perf_attrib_tear_sheet(returns,
                                  positions,
                                  factor_returns=None,
                                  factor_loadings=None,  #需要数据格式转换fator as index in pd.frame
                                  transactions=None,
                                  pos_in_dollars=True,
                                  factor_partitions=FACTOR_PARTITIONS,
                                  return_fig=False)"""        

"""pf.create_position_tear_sheet(returns, positions,
                               show_and_plot_top_pos=2, hide_positions=False,
                               sector_mappings=None, transactions=None,
                               estimate_intraday='infer', return_fig=False)
plt.show()"""

"""pf.create_txn_tear_sheet(returns, positions, transactions,
                          turnover_denom='AGB', unadjusted_returns=None,
                          estimate_intraday='infer', return_fig=False)
plt.show()"""


"""pf.create_round_trip_tear_sheet(returns, positions, transactions,
                                 sector_mappings=None,
                                 estimate_intraday='infer', return_fig=False)   #nested renamer is not supported
plt.show()"""


