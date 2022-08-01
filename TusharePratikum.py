import tushare as ts 
import pandas as pd
import numpy as np
pro = ts.pro_api(
    token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
df = pro.daily(ts_code='600009.SH', start_date='20220701',
               end_date='202208101').iloc[::-1]
#print(df.head())
#print(df1.head())
df1_20_max=df["close"].iloc[-24:-1].max()
df1_today=df["close"].iloc[0]
print("today close = ",df1_today,  "//20 day max =", df1_20_max)
if df1_today >= df1_20_max:
    print("Buy Buy Buy")
else:
    print ("No Buy Signal")

df1_10_min = df["low"].iloc[-10:-1].min()
df1_today_low= df["low"].iloc[0]
print("today low =", df1_today_low, "//10 day lowest=",df1_10_min)
if df1_today_low <= df1_10_min :
    print("Sell Sell Sell")
else:
    print("No Sell Signal")


data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
df_tscode =data["ts_code"]
print(df_tscode.head(),df_tscode.shape)