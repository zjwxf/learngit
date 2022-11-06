
import tushare as ts
ts_pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
#获取平安银行的历史数据
df = ts_pro.daily(ts_code='000001.SZ', start_date='20180101', end_date='20191230')
#逆序
df = df.reindex(index=df.index[::-1])
used_cols = ['trade_date', 'close']
df = df[used_cols]
df.to_csv('./000001.SZ.csv', index=None)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ffn
# 是否持仓
hold = False
# 持仓数
pos = 0
# 回测资金
capital = 100000
# 剩余资金
rest = 0
# 手续费万分之三
fee = 0.0003
# 每日资金数列表
capital_list = []
# 20日均线数组
MA20_array = np.zeros(20)
# 10日均线数组
MA10_array = np.zeros(10)
# 读取历史数据
df = pd.read_csv('./000001.SZ.csv')


#遍历历史数据
for i in range(len(df)):
	price = df.loc[i, 'close']
	date = df.loc[i, 'trade_date']
	# 价格序列乎移	
	MA10_array[0:9] = MA10_array[1:10]
	MA20_array[0:19] = MA20_array[1:20]
	# 将新数据追加到数组木端
	MA10_array[-1] = price
	MA20_array[-1] = price
	# 如果小于20个数据就跳过
	if i < 20:
		continue
	# 计算 MA 指标
	MA10 = MA10_array.mean()
	MA20 = MA20_array.mean()

# 判断是否达到开仓和平仓信号
if MA10 >= MA20 and hold == False:
	# 计算开仓数目
	pos = int(capital / price / 100)* 100
	# 剩余资金
	rest = capital - pos * price * (1 + fee)
	# 持仓设置为True
	hold = True
	print ('buy at', date, 'price', price, 'capital', capital)
elif MA10 < MA20 and hold == True:
	# 计算平仓后的资金
	capital = pos * price * (1 - fee) + rest
	# 持仓数设置为0
	pos = 0
	# 持仓设置为False
	hold = False
	print('sell at', date, 'price', price, 'capital', capital)


# 计算每日的资金数目
if hold == True:
	# 如果持仓，就记录当前市值
	capital_list.append(rest + pos * price)
else:
	# 如果没有持仓，就记录当前资金
	capital_list.append(capital)

# 将资金序列转换为 Series 对象
capital_series = pd.Series(capital_list)
# 计算资金序列的简单收益率
capital_returns = ffn.to_returns(capital_series)
# 计算收益率
print(ffn.calc_total_return(capital_series))
# 计算最大回撤率
print (ffn.calc_max_drawdown(capital_series))
# 计算夏普比率
print(ffn.calc_sharpe(capital_returns))
# 可视化资金曲线
plt.plot(range(len(capital_list)), capital_list)
plt.show()
