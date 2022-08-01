import yfinance as yf
import pandas as pd
import matplotlib
tesla= yf.Ticker("TSLA")
tesla_info =tesla.info
tesla_data = tesla.history(period="max")
tesla_data.head()
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


gme=yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())