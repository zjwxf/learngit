
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import tushare as ts
import pandas as pd
from IPython.display import (display, display_html, display_png, display_svg)
import matplotlib.pyplot as plt
import numpy as n

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


cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
results = cerebro.run()
print(results)
strat = results[0]
pyfoliozer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
# pyfolio showtime
import pyfolio as pf
#pf.create_full_tear_sheet(returns)
live_start_date ='2019-01-01'
pf.create_returns_tear_sheet(returns)
#plt.show()
#plt.figure()
plt.savefig('fig.png', bbox_inches='tight')
fig=plt.figure()
fig.set(alpha=0.2)
fig.tight_layout(pad=1, w_pad=1.0, h_pad=1.0)
#plt.show()
thestrats = cerebro.run()
thestrat = thestrats[0]
pyfolio = thestrat.analyzers._pyfolio.get_analysis()
def plot_strategy(pyfolio):
    returns = pyfolio['returns'].values()
    returns = pd.DataFrame(list(zip(pyfolio['returns'].keys(),pyfolio['returns'].values())), columns=['date','total_value'])
    

    sharpe = np.round(np.sqrt(252) * returns['total_value'].mean() / returns['total_value'].std(), 4)
    returns['total_value']=returns['total_value']+1
    returns['total_value'] = returns['total_value'].cumprod()
    annal_rtn = np.round(returns['total_value'].iloc[-1]**(252/len(returns))-1, 4)*100
    dd = 1-returns['total_value']/np.maximum.accumulate(returns['total_value'])
    end_idx = np.argmax(dd)
    start_idx = np.argmax(returns['total_value'].iloc[:end_idx])
    maxdd_days = end_idx-start_idx
    maxdd = np.round(max(dd), 4)*100
    
    returns = returns.set_index('date')
    ax=returns.plot(y='total_value')
    plt.text(0.01,0.8, f'sharpe: {sharpe:.2f}', transform=ax.transAxes)
    plt.text(0.01,0.75, f'maxdd: {maxdd:.2f}%', transform=ax.transAxes)
    plt.text(0.01,0.7, f'maxdd_days: {maxdd_days:}days', transform=ax.transAxes)
    plt.text(0.01,0.65, f'annal_rtn: {(annal_rtn):.2f}%', transform=ax.transAxes)
    plt.scatter([returns.index[start_idx], returns.index[end_idx]], [returns.iloc[start_idx], returns.iloc[end_idx]],
                s = 80, c = 'g', marker = 'v', label = 'MaxDrawdown Duration')
    plt.title('portfolio')
    plt.show()

