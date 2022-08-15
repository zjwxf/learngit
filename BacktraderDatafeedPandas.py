from __future__ import (absolute_import, division, print_function, unicode_literals)
import argparse
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas
import tushare as ts
from datetime import datetime as dt

pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
as_of_today = str(dt.now().strftime('%Y%m%d'))
def last_trading_day():
    data = pro.query('trade_cal',
                     start_date='20200101',
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

"""def maintask():
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
    x2 = data.pe < 50  # 市盈率低于100倍
    x3 = data.pb < 10  # 市净率低于10倍
    x4 = data.turnover_rate > 1  # 换手率大于1
    x = x1 & x2 & x3 & x4
    data_pool = data[x].ts_code
    print(len(data_pool))
    j = 1
    for i in data_pool:
        #time.sleep(0.1)
        j += 1
        df = pro.daily(ts_code = i, start_date = startdate, end_date = enddate, fields = 'ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount')
    return  df(i)"""

def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)
    #缺了时间的def
    data = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')
    AS_of_Today = int(dt.now().strftime('%Y%m%d'))
    data = data[data['list_date'].apply(int).values < (AS_of_Today-360)] #上市不足360日
    data = data[-data.name.str.startswith('*')]                          #*ST退市
    data = data[-data.industry.isin(['银行','保险','房地产','区域地产',])] #行业删除
    #pool = data.ts_code.values.tolist()
    #print(len(pool))
    data = pro.daily_basic(trade_date=last_trading_day())
    x1 = data.close < 200  # 收盘价小于200元
    x2 = data.pe < 50  # 市盈率低于100倍
    x3 = data.pb < 10  # 市净率低于10倍
    x4 = data.turnover_rate > 1  # 换手率大于1
    x = x1 & x2 & x3 & x4
    data_pool = data[x].ts_code
    print(len(data_pool))
    print(data_pool.head())
    #j = 1
    for i in data_pool:
        #time.sleep(0.1)
        #j += 1
        df = pro.daily(ts_code = i, start_date = '20220501', end_date = '20220802', fields = 'ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount')
    #return  df(i)
        return df 

    # Get a pandas dataframe
    #datapath = ('../../datas/2006-day-001.txt')
    datapath = df
    print(datapath)

    # Simulate the header row isn't there if noheaders requested
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0

    dataframe = pandas.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()