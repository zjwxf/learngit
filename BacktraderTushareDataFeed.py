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
cerebro.adddata(data)
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


