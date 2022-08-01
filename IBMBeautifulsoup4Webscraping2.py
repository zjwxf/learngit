import pandas as pd
import requests
from bs4 import BeautifulSoup
import bs4

url = "http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml"
data = requests.get(url).text
#data.encoding="utf-8"
soup = BeautifulSoup(data,'html5lib')
data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    data = data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)
print(data.head())
read_html_pandas_data = pd.read_html(url)
print(read_html_pandas_data)
#read_html_pandas_data = pd.read_html(str(soup))
#print(read_html_pandas_data)
soup.find("tbody").find_all('tr')
print(soup.find("tbody").find_all('tr'))