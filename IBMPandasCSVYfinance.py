"""f=open('d:\\backtrader\stock_data.csv',mode='r',encoding='utf-8')
r=f.read()
print(r)
f.close()

f=open('d:\\backtrader\\bt数据结构.png',mode='rb')     #路径\需要进行转义   rb打印视频文件
r=f.read()
print(r)"""

#import pandas as pd
#df=pd.read_csv("d:\\backtrader\stock_data.csv")
#print(df)
#print(df.size)
#print(df.shape)
#print(df.ndim)
#print(df.notnull)
#print(df.isnull)
#df.to_csv("d:\\backtrader\stock_data_2")
#df.to_csv("stock_data_3")


import yfinance as yf
import pandas as pd
import matplotlib as plt
apple = yf.Ticker("AAPL")
apple_info = apple.info
#print(apple_info)
#apple_info['country']
apple_share_price_data = apple.history(period="max")
apple_share_price_data.reset_index(inplace=True)
print(apple_share_price_data.head())
apple_share_price_data.plot(x="Date",y="Open")
#apple.dividends
#print(apple.dividends)
#apple.dividends.plot()