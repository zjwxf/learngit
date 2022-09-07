import os
import time
from datetime import datetime as dt
from datetime import timedelta
import threading
import pandas as pd
import numpy as np
import requests
import tushare as ts

pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
as_of_today = str(dt.now().strftime('%Y%m%d'))
def last_trading_day():
    data = pro.query('trade_cal',
                     start_date='20220101',
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
    #data = pro.query('stock_basic')
    data = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    AS_of_Today = int(dt.now().strftime('%Y%m%d'))
    data = data[data['list_date'].apply(int).values < (AS_of_Today-360)] #上市不足360日
    data = data[-data.name.str.startswith('*')]                          #*ST退市
    data = data[-data.industry.isin(['银行','保险','房地产','区域地产',])] #行业删除
    #pool = data.ts_code.values.tolist()
    #print(len(pool))
    data = pro.daily_basic(trade_date=last_trading_day())
    x1 = data.close < 200  # 收盘价小于200元
    x2 = data.pe < 30  # 市盈率低于100倍 参数PE <20,PB<5 411家， PE<30 PB<10 952家 
    x3 = data.pb < 10  # 市净率低于10倍
    x4 = data.turnover_rate > 1  # 换手率大于1
    x = x1 & x2 & x3 & x4
    data_pool = data[x].ts_code
    print("符合条件的股票总数:",len(data_pool))
    #print(data.head())  
   
    #pool = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    #print(pool.shape)
    #print(pool.ts_code.iloc[2000:2001])
    #print('获得上市股票总数：', len(pool)-1)
    j = 1
    #for i in pool.ts_code.iloc[4450:4845]:
    for i in data_pool.iloc[600:]:
        
        #time.sleep(0.1)

        j += 1

        df = pro.daily(ts_code = i,

        start_date = startdate,

        end_date = enddate,

        fields = 'ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol,amount')

    #df = pro.daily(ts_code= i, start_date='20220701',end_date='202208101').iloc[::-1]   #iloc[::-1]从后向前取，逆序
       
        if df["close"].iloc[0] < df['close'].iloc[1:21].min():  #df的date已经倒序今天为0，昨天为1， 0，1，2 今昨前
            k=1
            for k in range(1,51):
                df1_20_min=df["close"].iloc[k+1:k+51].min()
                df1_today=df["close"].iloc[k]
                if df1_today < df1_20_min:
                    #print(df['close'].iloc[1:25])
                    break
            else:
                #print(df['close'].iloc[1:21])
                #print(df.head())
                print(j,"Sell Sell Sell",'正在获取第%d家，股票代码%s.' % (j, i),"today close = ",df["close"].iloc[0],  "//20 day min =", df['close'].iloc[1:21].min())


        """df1_10_min = df["close"].iloc[-10:-1].min()
        df1_today_low= df["close"].iloc[0]
        if df1_today_low <= df1_10_min :
             print('正在获取第%d家，股票代码%s.' % (j, i), "today low =", df1_today_low, "//10 day lowest=",df1_10_min)
             print("Sell Sell Sell")
        else:
            pass"""
    return 



if __name__ == '__main__':
#设置起始日期
    startdate = '20220601'
    enddate = '20220901'
    #enddate = last_trading_day()
#主程序
maintask() 