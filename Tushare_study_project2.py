
# 导入tushare
import tushare as ts
# 初始化pro接口
pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')

# 拉取数据
df = pro.daily(**{
    "ts_code": "000001.SZ",
    "trade_date": "",
    "start_date": 20200101,
    "end_date": 20220101,
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
print(df.head())
df1= df["high"]
print(df1.tail())        
df2=df1.iloc[-50:-1]
print(df2.shape)
df2_max= df2.max()
print("max",df2_max)
df_if =df.loc[df["high"]>df2_max]
print(df_if)
