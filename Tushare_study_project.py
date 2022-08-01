

# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

# 拉取数据
df = pro.daily(**{
    "ts_code": "",
  
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
print(df.head(5))
print(df.shape)




"""import tushare as ts
import pandas as pd
import time

def maintask():
    pro = ts.pro_api(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

#获取基础信息数据，包括股票代码、名称、上市日期、退市日期等

    pool = pro.stock_basic(exchange = '',list_status = 'L',adj = 'qfq',fields = 'ts_code,symbol,name,area,industry,fullname,list_date, market,exchange,is_hs')

    print(pool.head())

    print('获得上市股票总数：', len(pool)-1)

    j = 1

    for i in pool.ts_code:

        #print('正在获取第%d家，股票代码%s.' % (j, i))

    #接口限制访问200次/分钟，加一点微小的延时防止被ban

        #time.sleep(0.301)

        j += 1

        df = pro.daily(ts_code = i,

        start_date = '20220101',

        end_date = '20220130',

        fields = 'ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount')

    print(df.head())
    #con1 = 'mysql+pymysql://tushare:pass@localhost:3306/stocks?charset=utf8'
    #df.to_sql(name="stocksname",con=con1,if_exists='replace',index=False)

    #writer = pd.ExcelWriter(i + '.xlsx')
    #df.to_excel(writer, sheet_name = i + '', index = False)
    df.to_csv('d:/backtrader/tushare_study_project.csv',index=False)
if __name__ == '__main__':

#设置起始日期

    #startdate = '19980101'

    #enddate = '20190304'

#主程序
  maintask()"""
