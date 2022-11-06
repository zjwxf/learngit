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

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=[6, 3]
plt.rcParams['figure.dpi']=200
plt.rcParams['figure.facecolor']='w'
plt.rcParams['figure.edgecolor']='k'

#使用tushare获取数据
#使用tushare旧版接口获取数据
"""def get_data(code,start,end):
    df=ts.get_k_data(code,autype='qfq',start=start,end=end)
    df.index=pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    return df
dataframe=get_data(code='sh',start='2010-01-01',end='2020-07-17')
print(dataframe.head())"""
#新版tushare
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
#df = pro.daily(ts_code='000001.SZ', start_date='2019101', end_date='20210101').iloc[::-1]
df = pro.daily(ts_code = '000088.SZ',start_date = '2017101',end_date = '20220801', fields = ' trade_date, open, high, low, close, vol')[::-1]
df.index=pd.to_datetime(df.trade_date)
df['openinterest']=0
#df.trade_date=pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
df=df[['trade_date','open','high','low','close','vol','openinterest']]
"""data = btfeeds.PandasData(
    dataname=df,
    fromdate=datetime(2000, 1, 1),
    todate=datetime(2021, 12, 31),
    datetime='trade_date',
    open='open',
    high='high',
    low='low',    
    close='close',
    volume='vol',
    openinterest=-1
)"""""

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
    #回测最优参数并画
    else:
        cerebro.addstrategy(TurtleStrategy,long_period=best_long,short_period=best_short)
        data = bt.feeds.PandasData(dataname=df)    
        cerebro.adddata(data)
        #broker设置资金、手续费
        cerebro.broker.setcash(startcash)
        cerebro.broker.setcommission(commission=com)
        #设置买入设置，策略，数量
        cerebro.addsizer(TradeSizer)
        #cerebro.addsizer(bt.sizers.FixedSize,stake=500)
        print('期初总资金: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        #cerebro.plot(iplot=False)
        cerebro.addobserver(bt.observers.DrawDown)
        cerebro.plot(volume=False)

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




# =============== 为系统注入数据 =================
#data = backtrader.feeds.PandasData(dataname=dataframe, fromdate=start_time, todate=end_time)  # 加载数据
cerebral_system = backtrader.Cerebro()
# 将数据传入回测系统
#cerebral_system.adddata(data)
#cerebral_system.addanalyzer(DailyReturnAnalyzer, _name="my_analyzer")
# 将交易策略加载到回测系统中
#cerebral_system.addstrategy(TurtleStrategy)
# =============== 系统设置 ==================
"""start_cash = 1000000
cerebral_system.broker.setcash(start_cash)
cerebral_system.broker.setcommission(commission=0.00025)  # 设置手续费 万2.5"""
#print('初始资金: {} 回测期间：from {} to {}'.format(start_cash, start_time, end_time))
# 运行回测系统
#cerebral_result = cerebral_system.run()
# 根据analyzer获得日收益率
#analyze_result = cerebral_result[0].analyzers[0].get_analysis()
#print(analyze_result)
"""————————————————
版权声明：本文为CSDN博主「呆萌的代Ma」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_35757704/article/details/125000894"""












"""# =========== for analysis.py ============ #
rets = pd.Series(strats.analyzers._TimeReturn.get_analysis())
pyfoliozer = strats.analyzers.getbyname("pyfolio")
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

perf_df = pyf.timeseries.perf_stats(returns, positions=positions, transactions=transactions)

returns.to_csv("./results/returns.csv")
positions.to_csv("./results/positions.csv")
transactions.to_csv("./results/transactions.csv")
gross_lev.to_csv("./results/gross_lev.csv")
perf_df.to_csv("./results/perf_df.csv")
rets.to_csv("./results/timereturn.csv", index=True)
# ======================================== #

cumrets = emp.cum_returns(rets, starting_value=0)
max_drawdown = emp.max_drawdown(rets)

ann_rets = emp.annual_return(rets, period="daily")
calmar_ratio = ann_rets / -max_drawdown
sharpe = emp.sharpe_ratio(rets, risk_free=0, period="daily")

# 盈亏比
mean_per_win = (rets[rets > 0]).mean()
mean_per_loss = (rets[rets < 0]).mean()

day_ret_max = rets.max()
day_ret_min = rets.min()

results_dict = {
    "年化夏普比率": sharpe,
    "最大回撤": max_drawdown,
    "累计收益率": cumrets[-1],
    "年化收益率": ann_rets,
    "收益回撤比": calmar_ratio,
    "单日最大收益": day_ret_max,
    "单日最大亏损": day_ret_min,
    "交易次数": len(transactions),
    "获胜次数": sum(rets > 0),
    "胜率": sum(rets > 0) / sum(rets != 0),
    "盈亏比": abs(mean_per_win / mean_per_loss),
}
results_series = pd.Series(results_dict)
print(pd.Series(results_series))
print(perf_df)


if __name__ == "__main__":
    run()
"""














"""
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import tushare as ts
import pandas as pd
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=5)
        sma2 = bt.ind.SMA(period=50)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

        self.atr = bt.ind.ATR(period=20)
    
        self.atr_max= self.atr.max()
        if self.atr[-1] >= self.atr_max:
            isbuy 
         
        print(atr)



cerebro = bt.Cerebro()
cerebro.broker.setcash(200000.0) # set the money
cerebro.addstrategy(SmaCross)
pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = pro.daily(ts_code='002020.SZ', start_date='2019101', end_date='20210101').iloc[::-1]
df.trade_date=pd.to_datetime(df.trade_date) #由于trade_date是字符串，BackTrader无法识别，需要转一下
data = btfeeds.PandasData(
    dataname=df,
    fromdate=datetime(2000, 1, 1),
    todate=datetime(2021, 12, 31),
    datetime='trade_date',
    open='open',
    high='high',
    low='low',    
    close='close',
    volume='vol',
    openinterest=-1
)
cerebro.adddata(data)
cerebro.run()
cerebro.plot(iplot=False)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

"""














