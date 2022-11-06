from datetime import datetime,timedelta
import backtrader as bt
import tushare as ts
import pandas as pd
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=[6, 3]
plt.rcParams['figure.dpi']=200
plt.rcParams['figure.facecolor']='w'
plt.rcParams['figure.edgecolor']='k'

# ts获取数据测试
#ts.get_k_data('601398',autype='qfq',start='2020-01-01',end='2022-05-25')
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = ts.pro_bar(ts_code= '399001.SZ', asset='I',start_date='19960101' , end_date='20221011',)


未完待续 ----------