"""
# 导入tushare
from matplotlib.pyplot import plot, xlabel, ylabel
import tushare as ts
import matplotlib.pyplot as plt
import seaborn as sns
# 初始化pro接口
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

# 拉取数据
df = pro.daily(**{
    "ts_code": "000001.SZ",
    "trade_date": "",
    "start_date": "",
    "end_date": "",
    "offset": "",
    "limit": ""
}, fields=[
    "ts_code",
    "trade_date",
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "change",
    "pct_chg",
    "vol",
    "amount"
])
print(df.tail(5))
df_high_price=df['high'].tail(200)
df_low_price = df['low'].tail(200)
df_trade_date=df['trade_date'].tail(200)
dfmax=df_high_price.max()
dfmin=df_low_price.min()
print("max",dfmax,"min",dfmin)
x=df_trade_date
yl=df_low_price
y=df_high_price
xlabel('X(trade_date)')
ylabel('Y(High-Price')
plt.plot(x,y,x,yl )
plt.show()"""




from datetime import datetime  #
# 导入backtrader框架
import backtrader as bt
import tushare as ts
import pandas as pd
import backtrader.feeds as btfeeds


# 创建策略继承bt.Strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close

    def next(self):
        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':
    # 创建Cerebro引擎
    cerebro = bt.Cerebro()
    # 为Cerebro引擎添加策略
    cerebro.addstrategy(TestStrategy)
    #填入自己的token
    pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
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
    cerebro.adddata(data)

    # 设置投资金额100000.0
    cerebro.broker.setcash(100000.0)
    # 引擎运行前打印期出资金
    print('组合期初资金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    # 引擎运行后打期末资金
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())
