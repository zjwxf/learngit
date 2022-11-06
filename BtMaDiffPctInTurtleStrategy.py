

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

"""plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=[6, 3]
plt.rcParams['figure.dpi']=200
plt.rcParams['figure.facecolor']='w'
plt.rcParams['figure.edgecolor']='k'"""


#新版tushare
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
#tushare指数要用到pro_bar
df = ts.pro_bar(ts_code='399006.SZ' ,asset='I',start_date ='20100101', end_date='20221010').iloc[::-1]
df.index=pd.to_datetime(df.trade_date)
df['openinterest']=0
#df.trade_date= pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
df=df[['trade_date','open','high','low','close','vol','openinterest']]
dataframe=df
print(dataframe)


#编写海龟策略+ MaDiffPct
class TurtleStrategy(bt.Strategy):
#默认参数
    params = (('long_period',100),
              ('short_period',5),  
              ('printlog', False), )   
    def __init__(self):        
        self.order = None      
        self.buyprice = 0      
        self.buycomm = 0      
        self.buy_size = 0      
        self.buy_count = 0       
        # 自定义指标MaDiffPct        
        self.Ma100_line = bt.indicators.SMA(self.data, period=self.p.long_period)       
        self.Ma5_line = bt.indicators.SMA(self.data, period=self.p.short_period)         
        self.MaDiff_line = (self.Ma5_line - self.Ma100_line)
        self.MaDiffPct_line= (self.MaDiff_line/self.Ma100_line)   
  
        self.buy_signal =bt.If(self.MaDiffPct_line <=-0.1,)  # self.MaDiffPct_line[-1] >self.MaDiffPct_line[0])       
        self.sell_signal = bt.If(self.MaDiffPct_line[0] >=0.03,)# self.MaDiffPct_line[-1]<self.MaDiffPct_line[0])   

    def next(self): 
        if self.order:
            return        
        #入场：价格突破上轨线且空仓时        
        if self.buy_signal  and self.buy_count == 0:                                 
            self.buy_size = self.broker.getvalue() * 0.2 
            #self.N =self.ATR[0]         
            self.buy_size  = int(self.buy_size  / 100) * 100                             
            self.sizer.p.stake = self.buy_size 
            self.buy_count = 1            
            self.order = self.buy()        
        #加仓：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）   ， self.ATR[0]? 加仓应该与首仓一样？？     
        elif  self.buy_count > 0 and self.buy_count <=4 and self.data.close >= self.buyprice*1.03 :    #上升加仓逻辑买入价的3%
            self.order = self.buy()           
            self.buy_count += 1        
        #elif  self.buy_count > 0 and self.buy_count <=4 and self.data.close <= self.buyprice*0.97 :    #下跌加仓逻辑买入价的3%
           # self.order = self.buy()           
            #self.buy_count += 1   
        #离场：价格跌破下轨线且持仓时        
        elif self.sell_signal  and self.buy_count > 0:            
            self.order = self.sell()            
            self.buy_count = 0        
        #止损：价格跌破买入价的2个ATR且持仓时        
        #elif self.buy_count > 0 and self.data.close < (self.buyprice - 2*self.N) :           
         #   self.order = self.sell()
          #  self.buy_count = 0   
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
                o:bt.Order=order
                
                # self.log(f'买入:\n价格:{order.executed.price},\
                # 成本:{order.executed.value:.2f},\
                # 手续费:{order.executed.comm:.2f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                # self.log(f'买入后总资金: {(self.broker.getvalue()-order.executed.value):.2f}')
                # self.log(self.broker.getposition(data))
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                size: {order.executed.size:.2f},\
                成本: {order.executed.value:.2f},\
                手续费{order.executed.comm:.2f}')
                self.log(f'卖出后总资金: {(self.broker.getvalue()):.2f}')
            self.bar_executed = len(self) 
        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'交易失败{order.status}')
        self.order = None
    #记录交易收益情况（可省略，默认不输出结果）？？？？？？？？
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

#编写回测主函数
#def main(df,long_list,short_list,best_long,best_short,startcash=1000000,com=0.001):
    #创建主控制器
if __name__ == '__main__':

    cerebro = bt.Cerebro() 
    cerebro.addstrategy(TurtleStrategy)
    data = bt.feeds.PandasData(dataname=df)    
    cerebro.adddata(data)
    #broker设置资金、手续费
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001, leverage =3)
    cerebro.addsizer(TradeSizer)
    #设置指标观察
 
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    print('期初总资金: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    results = cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(volume=False)



