import tushare as ts
import pandas as pd
pro = ts.pro_api(
    token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = pro.daily(ts_code='000001.SZ', start_date='20110101',
               end_date='20210101').iloc[::-1]
df.to_csv('stock_data.csv', index=False)



