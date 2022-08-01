
# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

# 拉取数据
df = pro.daily(**{
    "ts_code": "601688.SH",
    "trade_date": "",
    "start_date": "2010.01.01",
    "end_date": "2020.01.01",
    "offset": "",
    "limit": ""
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
df.to_csv('d:/backtrader/tushare_test2.csv')

        