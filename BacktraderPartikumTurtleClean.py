##导入相关包 优化jupyter画图设置
from datetime import datetime,timedelta
import backtrader as bt
import backtrader
import tushare as ts
import pandas as pd
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import backtrader.feeds as btfeeds
import efinance
from backtrader import Analyzer
#import pyfolio as pf             #pyfolio 绩效分析  https://blog.csdn.net/eryk86/article/details/110338377
import requests
import json 

#来源详解   https://blog.csdn.net/jsyzliuyu/article/details/125037530   https://www.sohu.com/a/478369954_505915   https://link.sov5.cn/l/lzgvCLgJvr

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=[6, 3]
plt.rcParams['figure.dpi']=200
plt.rcParams['figure.facecolor']='w'
plt.rcParams['figure.edgecolor']='k'


#新版tushare
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
#df = pro.daily(ts_code='000001.SZ', start_date='2019101', end_date='20210101').iloc[::-1]
df = pro.daily(ts_code = '000088.SZ',start_date = '2017101',end_date = '20220803', fields = ' trade_date, open, high, low, close, vol')[::-1]
df.index=pd.to_datetime(df.trade_date)
df['openinterest']=0
#df.trade_date=pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
df=df[['trade_date','open','high','low','close','vol','openinterest']]
dataframe=df
print(dataframe.head())


#编写海龟策略
class TurtleStrategy(bt.Strategy):
#默认参数
    params = (('long_period',20),
              ('short_period',10),  
              ('printlog', False), )   
    def __init__(self):        
        self.order = None      
        self.buyprice = 0      
        self.buycomm = 0      
        self.buy_size = 0      
        self.buy_count = 0       
        # 海龟交易法则中的唐奇安通道和平均波幅ATR        
        self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.long_period)        
        self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.short_period) 
        self.M_line = (self.H_line+self.L_line)/2
        self.TR = bt.indicators.Max((self.data.high(0)- self.data.low(0)),\
                                    abs(self.data.close(-1)-self.data.high(0)), \
                                    abs(self.data.close(-1)  - self.data.low(0)))        
        self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=14)       
        # 价格与上下轨线的交叉      
        self.buy_signal = bt.ind.CrossOver(self.data.close(0), self.H_line)        
        self.sell_signal = bt.ind.CrossOver(self.data.close(0), self.L_line)    
    def next(self): 
        if self.order:
            return        
        #入场：价格突破上轨线且空仓时        
        if self.buy_signal > 0 and self.buy_count == 0:                                 
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR            
            self.buy_size  = int(self.buy_size  / 100) * 100                             
            self.sizer.p.stake = self.buy_size             
            self.buy_count = 1            
            self.order = self.buy()        
        #加仓：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）        
        elif self.data.close >self.buyprice+0.5*self.ATR[0] and self.buy_count > 0 and self.buy_count <=4:           
            self.buy_size  = self.broker.getvalue() * 0.01 / self.ATR            
            self.buy_size  = int(self.buy_size  / 100) * 100            
            self.sizer.p.stake = self.buy_size             
            self.order = self.buy()           
            self.buy_count += 1        
        #离场：价格跌破下轨线且持仓时        
        elif self.sell_signal < 0 and self.buy_count > 0:            
            self.order = self.sell()            
            self.buy_count = 0        
        #止损：价格跌破买入价的2个ATR且持仓时        
        elif self.data.close < (self.buyprice - 2*self.ATR[0]) and self.buy_count > 0:           
            self.order = self.sell()
            self.buy_count = 0   
    #交易记录日志（默认不打印结果）
    def log(self, txt, dt=None,doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()},{txt}')
    #记录交易执行情况（默认不输出结果）
    def notify_order(self, order):
        # 如果order为submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')
            self.bar_executed = len(self) 
        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None
    #记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')
    def stop(self):
        self.log(f'(组合线：{self.p.long_period},{self.p.short_period})； \
        期末总资金: {self.broker.getvalue():.2f}', doprint=True)

#编写仓位管理函数
class TradeSizer(bt.Sizer):
    params = (('stake', 1),)    
    def _getsizing(self, comminfo, cash, data, isbuy):        
        if isbuy:          
            return self.p.stake        
        position = self.broker.getposition(data)        
        if not position.size:            
            return 0        
        else:            
            return position.size        
        return self.p.stake
#编写回测主函数
def main(df,long_list,short_list,best_long,best_short,startcash=1000000,com=0.001):
    #创建主控制器
    cerebro = bt.Cerebro()      
    #导入策略参数寻优
    if long_list:
        cerebro.optstrategy(TurtleStrategy,long_period=long_list,short_period=short_list)    
        #将数据加载至回测系统
        data = bt.feeds.PandasData(dataname=df)    
        cerebro.adddata(data)
        #broker设置资金、手续费
        cerebro.broker.setcash(startcash)
        cerebro.broker.setcommission(commission=com)
        #设置买入设置，策略，数量
        cerebro.addsizer(TradeSizer)
        #cerebro.addsizer(bt.sizers.FixedSize,stake=500)
        print('期初总资金: %.2f' % cerebro.broker.getvalue())
        cerebro.run(maxcpus=1)

    ###回测最优参数并画图
    else:
        cerebro.addstrategy(TurtleStrategy,long_period=best_long,short_period=best_short)
        data = bt.feeds.PandasData(dataname=df)    
        cerebro.adddata(data)
        #broker设置资金、手续费
        cerebro.broker.setcash(startcash)
        cerebro.broker.setcommission(commission=com)
        #设置指标观察
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        print('期初总资金: %.2f' % cerebro.broker.getvalue())
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')    
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        results = cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.plot(volume=False)

"""        strat = results[0]
        pyfoliozer = strat.analyzers.getbyname('pyfolio')
        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
        
            )
        

        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        results = cerebro.run()
        strat = results[0]
        pyfoliozer = strat.analyzers.getbyname('pyfolio')
        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
        # pyfolio showtime
        pf.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
            round_trips=True)
        plt.show()"""

        # At this point tables and chart will show up
"""# At this point tables and chart will show up
        results=cerebro.run()
        cerebro.plot(volume=False) 
        result = results[0]
        pyfolio = result.analyzers.pyfolio # 注意：后面不要调用 .get_analysis() 方法
        # 或者是 result[0].analyzers.getbyname('pyfolio')
        returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
        pf.create_full_tear_sheet(returns)"""


class DailyReturnAnalyzer(Analyzer):
    def __init__(self):
        super(DailyReturnAnalyzer, self).__init__()
        self.fund_record = []

    def next(self):
        self.fund_record.append(self.strategy.broker.getvalue())

    def get_analysis(self):
        fund_record_arr = np.array(self.fund_record)
        daily_return = np.diff(fund_record_arr) / fund_record_arr[0]
        return daily_return

        
    
#回测和参数调试
long_list=range(20,30,5)  #20天到70天 ，步进5
short_list=range(5,20,5)
main(dataframe,long_list=long_list,short_list=short_list,best_long=None,best_short=None)

#最优参数回测和画图 手动填写 long short 参数
main(dataframe,long_list=None,short_list=None,best_long=20,best_short=15)
