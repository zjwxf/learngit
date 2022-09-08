import os
import time
from datetime import datetime as dt
from datetime import timedelta
import threading
import pandas as pd
import numpy as np
import requests
import tushare as ts
import datetime 

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
    x2 = dataprice.pe < 20  # 市盈率低于100倍 参数PE <20,PB<5 411家， PE<30 PB<10 952家 
    x3 = dataprice.pb < 5  # 市净率低于10倍
    x4 = dataprice.turnover_rate > 1  # 换手率大于1
    X = x1 & x2 & x3 & x4
    dataprice=dataprice[X].ts_code
    data_pool= pd.merge(databasic,dataprice,on='ts_code') #merge df series的交集 data_pool是df, df定位iloc[0:,0]从0行开始，指定0列
    data_pool= data_pool.ts_code                          #转series object 定位iloc[0:]
    print("符合条件的股票总数:",len(data_pool), "最后交易日：", last_trading_day(),'enddate:', enddate)

    j = 1
    for i in data_pool.iloc[0:]:
        j += 1
        df = pro.daily(ts_code = i,start_date = startdate, end_date = enddate,fields = 'ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol,amount')
        if df["close"].iloc[0] < df['close'].iloc[1:21].min():  #df的date已经倒序今天为0，昨天为1， 0，1，2 今昨前
            k=1
            for k in range(1,51):
                df1_20_min=df["close"].iloc[k+1:k+51].min()
                df1_today=df["close"].iloc[k]
                if df1_today < df1_20_min:
                    break
            else:
                print(j,"Sell Sell Sell",'正在获取第%d家，股票代码%s.' % (j, i),"today close = ",df["close"].iloc[0],  "//20 day min =", df['close'].iloc[1:21].min())
    return 



if __name__ == '__main__':
#设置起始日期
    startdate = '20220601'
    #enddate = '20220901'
    enddate = last_trading_day()
#主程序
maintask() 