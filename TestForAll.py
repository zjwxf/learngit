"""from dataclasses import dataclass
import os
from re import S
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime 
import threading
import pandas as pd
import numpy as np
import requests
import tushare as ts

pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')



df = pro.stock_basic(**{
    "ts_code": "000001.SZ ,601318.SH,839790.BJ,688596.SH,002411.SZ",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "market",
    "list_date"
])
print(df,'#'*40)
now = datetime.datetime.now()
delta = datetime.timedelta(days=360)
df['list_date']=pd.to_datetime(df['list_date'])
df = df[df['list_date'] < (now- delta)]
print(df)
df=df[df.market.isin(['主板','创业板'])]
print(df)
df = df[~df.industry.isin(['银行'])]
print(df)
df = df[~df.name.str.startswith('*')]  
print(df)
#
data1= pro.daily_basic(ts_code='', trade_date='20220905', fields='ts_code,trade_date,,close,turnover_rate,volume_ratio,pe,pb')
print(data1)"""


        

"""from dataclasses import dataclass
import os
from re import S
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime 
import threading
import pandas as pd
import numpy as np
import requests
import tushare as ts

pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
as_of_today = str(dt.now().strftime('%Y%m%d'))
def last_trading_day():
    data = pro.query('trade_cal',
                     start_date='20000101',
                     end_date=as_of_today,
                     is_open='1')
    trading_dates = data['cal_date']
    d0 = dt.now()
    trading_dates_list = trading_dates.tolist()

    if as_of_today in trading_dates.values:
        if d0.hour >= 16:
            today_index = trading_dates_list.index(as_of_today)
            latest_trading_date = trading_dates_list[int(today_index)]
            return latest_trading_date
        else:
            previous_trading_date = trading_dates.values[-2]
            return previous_trading_date
    else:
        previous_trading_date = trading_dates.values[-1]
        return previous_trading_date
def maintask():
    databasic = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    #时间今天-360天>上市日期
    now = datetime.datetime.now()        #last_trading_day()和now不冲突
    delta = datetime.timedelta(days=360)
    databasic['list_date']=pd.to_datetime(databasic['list_date'])
    databasic = databasic[databasic['list_date'] < (now- delta)]
    #板块分类
    databasic = databasic[~databasic.name.str.startswith('*')]                          #*ST退市
    #databasic = databasic[~databasic.ts_code.str.endswith('BJ')]
    databasic = databasic[~databasic.industry.isin(['银行','保险','房地产','区域地产',])] #行业删除
    #databasic=databasic[~databasic.market.isin(['CDR','北交所','科创板',])]
    databasic=databasic[databasic.market.isin(['主板','创业板','中小板','科创板'])]
    databasic=databasic.ts_code         #databasic=databasic['ts_code'] 这两个表达式一样

    #价格数据分类
    dataprice = pro.daily_basic(trade_date=enddate)    
    x1 = dataprice.close < 200  # 收盘价小于200元
    x2 = dataprice.pe < 200  # 市盈率低于100倍 参数PE <20,PB<5 411家， PE<30 PB<10 952家 
    x3 = dataprice.pb < 10  # 市净率低于10倍
    x4 = dataprice.turnover_rate > 1  # 换手率大于1
    X = x1 & x2 & x3 & x4
    dataprice=dataprice[X].ts_code
    data_pool= pd.merge(databasic,dataprice,on='ts_code') #merge df series的交集 data_pool是df, df定位iloc[0:,0]从0行开始，指定0列
    data_pool= data_pool.ts_code                          #转series object 定位iloc[0:]
    print("符合条件的股票总数:",len(data_pool), "最后交易日：", last_trading_day(),'enddate:', enddate)

    j = 1
    for i in data_pool.iloc[0:]:  #仅代码列表的df,iloc[0:,0]从0行开始，指定0列
        j += 1 
        df = ts.pro_bar(ts_code= i, start_date=startdate , end_date=enddate, ma=[5, 20, 50])
        #print(df)
        df=df.loc[0:30,['ts_code','close','trade_date',"ma5","ma20"]] # 取行，列
        #print(df.head())
        if df.isna().values.any()==True  and  df.isnull().values.any()==True : # 查看所有数据中是否有NaN最快的，没有输出False，反之为True：
            print('Erro第%d家股票代码%s.' % (j, i))
            continue
        elif df["ma5"].iloc[0] < df['ma20'].iloc[0] :
            ok=True
            for k in range(0,21):
                if df['ma5'].iloc[k+1] < df['ma20'].iloc[k+1]: 
                    ok= False
                    break
            if ok:
                    print("Cross Down",'第%d家，股票代码%s.' % (j, i),"today close = ",df["close"].iloc[0],  "MA5 =", df['ma5'].iloc[0], "MA20 =",df['ma20'].iloc[0])
    return 
if __name__ == '__main__':
    startdate = '20220501'
    enddate = last_trading_day()
   
maintask() 
"""


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


df = ts.pro_bar(ts_code= '399006.SZ', asset='I',start_date='20000101' , end_date='20221010', ma=[5, 20, 100])
print(df.head())
#指数调用
#df = pro.index_daily(ts_code='399006.SZ', start_date='20200101' , end_date='20220901', ma=[5, 20, 100])
#df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
df=df[['trade_date', 'close','ma5','ma20','ma100']]
df["diff"] = df['ma5']-df['ma100']
df['diff_pct'] =df['diff']*100/df['ma100']
df=df[df['diff_pct']<= 0]
df=df[df['diff_pct']<=-10]
print(df.head())

databasic = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
df_basic=databasic[['ts_code','industry']]
#industry_group= df_basic.groupby('industry')['ts_code'].count()
industry_value=databasic['industry'].value_counts() #indusry下各类别的数目
#industry_group=pd.DataFrame(industry_group)
pd.set_option('display.max_rows', None)
#print(industry_group)
#print(industry_value)
df2=databasic.groupby(['area'])['industry'].value_counts(normalize=True)  #分类area下industry各类的百分比
#print(df2)

Feature = databasic['industry']
Feature = pd.concat([Feature,pd.get_dummies(databasic['area'])], axis=1)
#Feature.drop(['Master or Above'], axis = 1,inplace=True)
pd.set_option('display.max_rows', None)
#print(Feature)

X = databasic[['industry','area','market']].values
pd.set_option('display.max_rows', None)
#print(X)
#print(X[0:5])


"""for i in range(110):
    databasic['industry'].replace(   ,i,  inplace= True)
    databasic['industry']=i
    df['attr_1'].replace('场景.季节.冬天', '冬天', inplace=True)
"""

#print(industry_group.set_option('display.max_rows',None))
#print(list(industry_group).count)
#print(df_basic.groupby('industry').groups)


#画图
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
#sns.lineplot(x='trade_date',y='diff_pct',data=df,legend='full',hue="ma5")
#sns.lineplot(x="trade_date",y='close',data=df,legend='brief')
#sns.lineplot(x="trade_date",y='ma5',data=df)
#sns.lineplot(x="trade_date",y='ma100',data=df)

#sns.relplot(x="trade_date",y="diff_pct",kind="line",data=df)
#sns.relplot(x="trade_date",y="ma100",kind="line",data=df)
#plt.show()

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
#data = np.arange(0,1,0.01) #伪造从0到1以0.01为增量的数据
#plt.title('MA-Close Diff') #写上图题
#plt.xlabel('trade_date') #为x轴命名为“x”
#plt.ylabel('price') #为y轴命名为“y”
#plt.xlim(0,1) #设置x轴的范围为[0,1]
#plt.ylim(0,1) #同上
#plt.xticks([0,0.2,0.4,0.6,0.8,1]) #设置x轴刻度
#plt.yticks([0,0.2,0.4,0.6,0.8,1]) #设置y轴刻度
#plt.tick_params(labelsize = 20) #设置刻度字号
#plt.plot(data,data**2) #第一个data表示选取data为数据集，第二个是函数，data的平方
#plt.plot(data,data) #同上
#plt.legend(['y = x^2','y = x^3']) #打出图例
#plt.show() #显示图形

df=df.iloc[::-1]
print(df.head())
plt.figure(figsize=[20,9])#设置图像宽高
plt.title("MA_Diff Relationship",fontsize=24,color='b')
plt.xlabel("trade_Date",fontsize=14,color='b')
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