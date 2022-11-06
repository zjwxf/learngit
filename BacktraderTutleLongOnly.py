

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
import backtrader.indicators as btind
from datetime import datetime as dt

#来源详解   https://blog.csdn.net/jsyzliuyu/article/details/125037530   https://www.sohu.com/a/478369954_505915   https://link.sov5.cn/l/lzgvCLgJvr

#新版tushare
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
as_of_today = str(dt.now().strftime('%Y%m%d'))
print('Today :' , as_of_today)
#设置参数
startdate = '20100101'
enddate = as_of_today  
setcode= '399673.SZ'
codetype=  'I' #'I' #'E'
#df = ts.pro_bar(ts_code=setcode ,asset='I',start_date = startdate , end_date = enddate).iloc[::-1]
df = ts.pro_bar(ts_code=setcode ,asset=codetype,start_date = startdate , end_date = enddate,).iloc[::-1]
#tushare指数要用到pro_bar  #399001 资金需要设置为1000万
#df = ts.pro_bar(ts_code='399006.SZ' ,asset='I',start_date ='20160101', end_date='20221022',).iloc[::-1]
#df = ts.pro_bar(ts_code='159949.SZ' ,asset='FD',start_date ='20100101', end_date='20221022',).iloc[::-1]
df.index=pd.to_datetime(df.trade_date)
df['openinterest']=0
#df.trade_date= pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
df=df[['trade_date','open','high','low','close','vol','openinterest']]
#增加画图的数据来源
#df1 = ts.pro_bar(ts_code='000300.SH' ,asset='I',start_date = startdate , end_date = enddate,).iloc[::-1]
#df1.index=pd.to_datetime(df.trade_date)
#df1['openinterest']=0
#df1=df1[['trade_date','open','high','low','close','vol','openinterest']]
#编写策略
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
        self.H_line = bt.indicators.Highest(self.data.high(-1), period=self.p.long_period,) #plot=False)       
        self.L_line = bt.indicators.Lowest(self.data.low(-1), period=self.p.short_period, ) #plot=False)         
        self.M_line = (self.H_line+self.L_line)/2
        self.TR = bt.indicators.Max((self.data.high(0)- self.data.low(0)),\
                                    abs(self.data.close(-1)-self.data.high(0)), \
                                    abs(self.data.close(-1)  - self.data.low(0)))   
        #SMA 和 EMA 对比结果差异较大 在有Leverage=3的情况下SMA的收益率340%，EMA收益率129%    测试EMA下 leverage= 参数无作用？？  EMA periode=19 25 30效果明显？？？                      
        self.ATR = bt.indicators.SimpleMovingAverage(self.TR, period=20)    
       
        #self.ATR = bt.indicators.ATR(self.data, period=20) 
        #self.ATR = bt.indicators.EMA(self.TR, period=29)   
        # 价格与上下轨线的交叉      
        self.buy_signal = bt.ind.CrossOver(self.data.close(0), self.H_line, plot=False)        
        self.sell_signal = bt.ind.CrossOver(self.data.close(0), self.L_line, plot=False)
    def next(self): 
        # Access -1, because drawdown[0] will be calculated after "next"
        #self.log('DrawDown: %.2f' % self.stats.drawdown.drawdown[-1])
        #self.log('MaxDrawDown: %.2f' % self.stats.drawdown.maxdrawdown[-1])
        if self.order:
            return        
        #入场：价格突破上轨线且空仓时        
        if self.buy_signal > 0 and self.buy_count == 0:        
            #原仓位控制 Value/N                         
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR     
            #等仓位20% Maxsize=5 未考虑margin
            #self.buy_size = int(self.broker.getvalue() / self.data.close)*0.2   
            self.N =self.ATR[0]         
            self.buy_size  = int(self.buy_size  / 100) * 100                             
            self.sizer.p.stake = self.buy_size      #0.1是缩小仓位为10%==或者等于10倍杠杆
            self.buy_count = 1            
            self.order = self.buy()     
            self.buyprice=self.buyprice   
            print(self.data.datetime.time(0),'N =', self.N, 'Buysize=',self.buy_size)

            #print('成交日期',self.data.datetime.date[0])
            """print('买入 N/ATR==', '%.2f' % self.N )
            print('ClosePrice ==', self.buyprice)
            print('仓位',self.sizer.p.stake, self.buy_size)
            print('加仓买入金额',self.sizer.p.stake * self.buyprice)
            print("买入金额比例",'{:.2%}'.format(self.sizer.p.stake *self.buyprice/10000000))
            print('资产', '%.2f' % self.broker.getvalue())
            print('资金', '%.2f' % self.broker.getcash())
            """
        
            
        #加仓：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）   ， self.ATR[0]? 加仓应该与首仓一样？？     
        elif  self.buy_count > 0 and self.buy_count <=4 and self.data.close >self.buyprice + 0.5*self.N :   
            self.order = self.buy()          
            self.buy_count += 1
            """print('加仓', self.sizer.p.stake) 
            print('加仓买入金额',self.sizer.p.stake * self.buyprice)
            print('资产', '%.2f' % self.broker.getvalue())
            print('资金', '%.2f' % self.broker.getcash())"""

        #离场：价格跌破下轨线且持仓时  ,离场应该是盈利的，实测都不盈利？？？   增加条件 count >=2时候用离场策略即价格低于10天下线   
        elif self.sell_signal < 0  and self.buy_count >= 2:               
            self.order = self.sell()            
            self.buy_count = 0  
            """print('离场') 
            print('资产', '%.2f' % self.broker.getvalue())
            print('资金', '%.2f' % self.broker.getcash())"""
            
             
        #止损：价格跌破买入价的2个ATR且持仓时. 分布建仓的情况下，平均买入价-2ART=止损价？？        
        elif self.buy_count > 0 and self.data.close < (self.buyprice - 2*self.N)  and self.buy_count<=1:           
            self.order = self.sell()
            self.buy_count = 0   
            """print('止损')
            print('资产', '%.2f' % self.broker.getvalue())
            print('资金', '%.2f' % self.broker.getcash())"""
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
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}, 收益率{(trade.pnlcomm/self.broker.getvalue()):.2f}')
    def stop(self):
        self.log(f'(组合线：{self.p.long_period},{self.p.short_period})； \
        期末总资金: {self.broker.getvalue():.2f}', doprint=True)
        self.log('MaxDrawDown: %.2f' % self.stats.drawdown.maxdrawdown[-1])
        

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
    #回测数据
    cerebro = bt.Cerebro() 
    cerebro.addstrategy(TurtleStrategy)
    data = bt.feeds.PandasData(dataname=df)    
    cerebro.adddata(data)
    #同轴多数据、
    """data1 = bt.feeds.PandasData(dataname=df1)
    data1.compensate(data)  # let the system know ops on data1 affect data0
    data1.plotinfo.plotmaster = data
    data1.plotinfo.sameaxis = False
    cerebro.adddata(data1)"""

    #broker设置资金、手续费
    cerebro.broker.setcash(10000000)
    cerebro.addsizer(TradeSizer)
    #设置指标观察
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)
    #cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    #cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years,data=data, _name='datareturns')
    #cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)
    
    #cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, _name='timereturns')
    #cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    strat0 = results[0]
    
    tret_analyzer = strat0.analyzers.getbyname('timereturn')
   #print(tret_analyzer.get_analysis())
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(volume=False)


#bt.observers.DrawDown
