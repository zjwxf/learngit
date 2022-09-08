from dataclasses import dataclass
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
                     start_date= startdate,
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
    
    data = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    #AS_of_Today = int(dt.now().strftime('%Y%m%d'))
    #dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #AS_of_Today =datetime.datetime.now().strftime('%Y-%m-%d')
    #print(len(data))
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=360)
    data['list_date']=pd.to_datetime(data['list_date'])
    #print[data['list_date']]
    #df['time'] = pd.to_datetime(df['time'])
    #df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    #delta =AS_of_Today - data['list_date']
    data = data[data['list_date'] < (now- delta)]
    #print(data.info())
    #data = data[data['list_date'].apply(int).values < (AS_of_Today-700)] #上市不足360日 688416.SH 上市不足10天，没有被筛选排除出来

    #print(data['list_date'].apply(int).values)
    #print(as_of_today)
    #print(AS_of_Today-700)

    data = data[~data.name.str.startswith('*')]                          #*ST退市
    data = data[~data.ts_code.str.endswith('BJ')]
    data = data[~data.industry.isin(['银行','保险','房地产','区域地产',])] #行业删除
    #print(len(data))  #print(data.info)
    data=data[~data.market.isin(['CDR','北交所','科创板',])]
    data=data[data.market.isin(['主板','创业板','中小板'])]
    
    #print(df.filter(items=['北交所', '科创板']))
    #data=data[data.exchange.isin(['SSE上交所', 'SZSE深交所'])]
    #print(len(data))   #print(data.info)
    #print(data.info())
    #print(data['market'].groupby)
    #print(data['market'].count)
    #pool = data.ts_code.values.tolist()
    #print(len(pool)
    data = pro.daily_basic(trade_date=last_trading_day())    #pro.dailly_basic是日系数据接口
    x1 = data.close < 200  # 收盘价小于200元
    x2 = data.pe < 20  # 市盈率低于100倍 参数PE <20,PB<5 411家， PE<30 PB<10 952家 
    x3 = data.pb < 5  # 市净率低于10倍
    x4 = data.turnover_rate > 1  # 换手率大于1
    x = x1 & x2 & x3 & x4
    data_pool = data[x].ts_code  #仅代码列表
    print(data_pool.info)
    print("符合条件的股票总数:",len(data_pool))

    #df = ts.pro_bar(ts_code='300219.SZ', start_date=startdate, end_date=enddate, ma=[5, 20, 50])
    #df=df.dropna()
    #print(df)
    #print(data.head())  
    #pool = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    #print(pool.shape)
    #print(pool.ts_code.iloc[2000:2001])
    #print('获得上市股票总数：', len(pool)-1)
    j = 1
    #for i in pool.ts_code.iloc[4450:4845]:
    for i in data_pool.iloc[0:]:  #275到281都有问题
        #time.sleep(0.1)
        j += 1  
    #df = pro.daily(ts_code= i, start_date='20220701',end_date='202208101').iloc[::-1]   #iloc[::-1]从后向前取，逆序
        df = ts.pro_bar(ts_code= i, start_date=startdate , end_date=enddate, ma=[5, 20, 50])
        #print(df.info)
        
        df=df.loc[0:30,['ts_code','close','trade_date',"ma5","ma20"]] # 取行，列
        #print(df)
        #print(df.head())
        
        
        if df.isna().values.any()==True  and  df.isnull().values.any()==True : # 查看所有数据中是否有NaN最快的，没有输出False，反之为True：
            print('Erro第%d家，股票代码%s.' % (j, i))
            continue
        #df的date已经倒序今天为0，昨天为1(dataframe 从上向下排列， 0，1，2 今昨前
                # and df['ma5'].iloc[0]> df['ma50'].iloc[0]:  
            #首次突破
        elif df["ma5"].iloc[0] > df['ma20'].iloc[0] :
            #print('j=',j,'ma5=',df['ma5'].iloc[0],'ma20=',df['ma20'].iloc[0] )
            ok=True
            for k in range(0,21):
                if df['ma5'].iloc[k+1] > df['ma20'].iloc[k+1]: 
                    #print(df['ma5'].iloc[k+1],df['ma20'].iloc[k+1])
                    ok= False
                    break
            if ok:
                    print("Cross Up",'第%d家，股票代码%s.' % (j, i),"today close = ",df["close"].iloc[0],  "MA5 =", df['ma5'].iloc[0], "MA20 =",df['ma20'].iloc[0])
    return 





if __name__ == '__main__':
#设置起始日期
    startdate = '20200501'
    enddate = '20220901'
    #enddate = last_trading_day()
#主程序
maintask() 