
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


pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = ts.pro_bar(ts_code= '399001.SZ', asset='I',start_date='20100101' , end_date='20221025', ma=[5, 20, 100])
df=df[['trade_date', 'close','ma5','ma20','ma100']]
df["diff"] = df['ma5']-df['ma100']
df['diff_pct'] =df['diff']*100/df['ma100']
#df=df[df['diff_pct']<= 0]
#df=df[df['diff_pct']<=-10]
#print(df.head(100))
df=df.iloc[::-1]

open=False
open_price=0
last_state=0
new_df=pd.DataFrame()
for ind, row in df.iterrows():
  if row['diff_pct'] > 0: #偏差大于上限
    state = 1
  elif row['diff_pct']<-15:  #偏差小于下限
    state=-1
  else:
    state=0
  if open==False and last_state!=-1 and state==-1:
    row['profit']=0
    open_price=row['close']
    new_df=new_df.append(row)
    open=True
  elif open==True and last_state!=1 and state==1:  #
    row['profit']=row['close']-open_price
    row['pct']=row['profit']*100/open_price
    new_df=new_df.append(row)
    open=False
  last_state = state
pd.set_option('display.max_rows', None) 
print(new_df)
df=new_df
  


#画图
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

#df=df.iloc[::-1]
#print(df.head())
plt.figure(figsize=[20,9])#设置图像宽高
plt.title("MA_Diff Relationship",fontsize=24,color='b')
plt.xlabel("trade_Date",fontsize=14,color='b')
plt.ylabel("Price",fontsize=14,color='b')
x=df['trade_date']
plt.plot(x,df['ma5'],label="MA5",color="b")
plt.plot(x,df['ma100'],label="MA100",color="g")
plt.plot(x,df['close'],label="Close",color="y")
plt.legend ()


x_major_locator=MultipleLocator(5)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(200)
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

plt.show()     #显示图片，如果注释改行，即使设置了图片仍然不显示"""