import pandas as pd
from yfinance import download 
download ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv","auto.csv")
path = "auto.csv"
df = pd.read_csv(path,headers=None)
print("The first 5 rows of the dataframe") 
df.head(5)

# create headers list
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
print("headers\n", headers)

df.columns = headers
df.head(10)

#We need to replace the "?" symbol with NaN so the dropna() can remove the missing values
df1=df.replace('?',np.NaN)
df=df1.dropna(subset=["price"], axis=0)
df.head(20)

df.describe(include = "all")
df[['length', 'compression-ratio']].describe()




