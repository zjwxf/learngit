from cProfile import label
from dataclasses import dataclass
import os
from re import S
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime 
import threading
from winreg import HKEY_USERS
import pandas as pd
import numpy as np
import requests
import tushare as ts
from matplotlib import pyplot as plt
import seaborn as sns
#sns.lineplot(x='trade_date',y='diff_pct',data=df,legend='full',hue="ma5")
#sns.lineplot(x="trade_date",y='close',data=df,legend='brief')
#sns.lineplot(x="trade_date",y='ma5',data=df)
#sns.lineplot(x="trade_date",y='ma100',data=df)
#sns.relplot(x="trade_date",y="diff_pct",kind="line",data=df)
#sns.relplot(x="trade_date",y="ma100",kind="line",data=df)
#plt.show()


pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
as_of_today = str(dt.now().strftime('%Y%m%d'))
def last_trading_day():
    data = pro.query('trade_cal',
                     start_date='20000101',#这个只是pro.query内有效
                     end_date=as_of_today,
                     is_open='1')
    trading_dates = data['cal_date']
    d0 = dt.now()
    trading_dates_list = trading_dates.tolist()
#设置起始日期
startdate = '20000101'
enddate = last_trading_day()  #enddate = '20220901 自定义日期'
df = ts.pro_bar(ts_code= '399001.SZ',asset='I',start_date = startdate , end_date = enddate, ma=[5, 20, 100])   #000016.SH 上证50 指数 asset='I' 
#df = ts.pro_bar(ts_code= '159920.SZ',asset='FD',start_date='20100101' , end_date='20221025', ma=[5, 20, 100])   #基金 asset = 'FD'

df=df[['trade_date', 'close','ma5','ma20','ma100']]
df["diff"] = df['ma5']-df['ma100']
df['diff_pct'] =df['diff']*100/df['ma100']



from matplotlib.pyplot import MultipleLocator

df=df.iloc[::-1]
print(df[['trade_date','diff_pct','close']].head())
plt.figure(figsize=[20,9])#设置图像宽高
plt.title("MA_Diff Relationship",fontsize=24,color='b')
plt.xlabel("Trade_Date",fontsize=14,color='b')
plt.ylabel("Price",fontsize=14,color='b')
x=df['trade_date']
plt.plot(x,df['ma5'],label="MA5",color="b")
plt.plot(x,df['ma100'],label="MA100",color="g")
#plt.plot(x,df['diff'],label="Diff",color="g")
#plt.plot(x,df['diff_pct'],label="Diff-Pct",color="y")
plt.plot(x,df['close'],label="Close",color="y")
plt.legend ()


x_major_locator=MultipleLocator(200)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(100)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)

#双Y坐标
z_ax = ax.twinx() # 创建与轴群ax共享x轴的轴群z_ax
z_ax.plot(x, df['diff_pct'],label="Diff_pct", color='r')
z_ax.set_ylabel('Precentage %',color='r',fontsize=14)
plt.legend(loc=4)   #显示图例，如果注释改行，即使设置了图例仍然不显示

plt.show()     #显示图片，如果注释改行，即使设置了图片仍然不显示




#Ma100要有分析对象前100天数据，经常要数据缺失
"""dfm=df.nlargest(1,'close') #找出最高/低值，确认位置，分析位置前后20天的情况
#print(dfm)
date_of_max_close= dfm.iat[0,0]
date_of_max_close=pd.to_datetime(date_of_max_close)  
index_of_max =dfm.index
index_number = index_of_max[0]
#print(index_number)
#print(index_of_max)
#print(date_of_max_close)
k= index_number
list_of_ma_diff=[]
for i in range(-20,20):
    diff_ma5_ma100 =(df['ma5'].iloc[i+k] - df['ma100'].iloc[i+k])/df['ma100'].iloc[i+k]
    diff_ma5_ma100=diff_ma5_ma100
    list_of_ma_diff.append(diff_ma5_ma100)
#print(list_of_ma_diff)
dataframe= pd.DataFrame(list_of_ma_diff)
#print(dataframe.iloc[15:25])

list_of_ma_diff= []
for j in range(-20,21):
    diff_ma5_ma100=df['diff'].iloc[j+k]
    list_of_ma_diff.append(diff_ma5_ma100)
df_diff_K_index =pd.DataFrame(list_of_ma_diff)
#print(df_diff_K_index)"""
