
# 导入tushare
import tushare as ts
import pandas as pd
import pymysql

# 初始化pro接口
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

# 拉取数据
df = pro.stock_basic(**{
    "ts_code": "",
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
print(df.head(5))

con1 = 'mysql+pymysql://tushare:pass@localhost:3306/stocks?charset=utf8'
df.to_sql(name="stocksname",con=con1,if_exists='replace',index=False)



        