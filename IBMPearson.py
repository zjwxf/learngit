from unicodedata import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
df = pd.read_csv("C:/Users/HW\Downloads/automobileEDA.csv")
#df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv")
"""print(df.head())
print(df.dtypes)
print(df["peak-rpm"].corr(df["gas"]))            #df["columm"].corr(["column"])
df1=df.select_dtypes(include=['float64'])
df2=df.select_dtypes(include=['int64'])
print(df1.corr())
print(df2.corr())
df3=df[['bore','stroke','compression-ratio','horsepower']].corr()
print(df3)"""

"""sns.regplot(x="engine-size", y="price", data=df, ci=68,x_estimator=np.mean, truncate=True,color="g")   #致信区间 68% ci=68 ,#用离散x变量绘制图，显示唯一值的平均值和置信区间
plt.ylim(0,)                                     #ylim(0,100)  y轴的范围
plt.show()"""

"""sns.boxplot(x="body-style", y="price", data=df)
plt.show()"""

"""print(df.describe())  #describe function automatically computes basic statistics for all continuous variables. Any NaN values are automatically skipped in these statistics"""


"""print(df['drive-wheels'].value_counts().to_frame())   #"value_counts" only works on pandas series, not pandas dataframes. how many units of each characteristic/variable"""


""""# grouping results
df_gptest = df[['drive-wheels','body-style','price']]
grouped_test1 = df_gptest.groupby(['drive-wheels','body-style'],as_index=False).mean()
print(grouped_test1)

grouped_pivot = grouped_test1.pivot(index='drive-wheels',columns='body-style')
print(grouped_pivot)

grouped_pivot = grouped_pivot.fillna(0) #fill missing values with 0
print(grouped_pivot)


print(df[["body-style","price"]].groupby(["body-style"],as_index=False).mean())  # "groupby" function to find the average "price" of each car based on "body-style".


#use the grouped results
plt.pcolor(grouped_pivot, cmap='RdBu')                 #heat map
plt.colorbar()
plt.show()


fig, ax = plt.subplots()
im = ax.pcolor(grouped_pivot, cmap='RdBu')
#label names
row_labels = grouped_pivot.columns.levels[1]
col_labels = grouped_pivot.index
#move ticks and labels to the center
ax.set_xticks(np.arange(grouped_pivot.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(grouped_pivot.shape[0]) + 0.5, minor=False)
#insert labels
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(col_labels, minor=False)
#rotate label if too long
plt.xticks(rotation=90)
fig.colorbar(im)
plt.show()"""

from scipy import stats
pearson_coef, p_value = stats.pearsonr(df['wheel-base'], df['price'])                              #p_value ;pearson correlation coefficent is linear relationship
print("The Pearson Correlation Coefficient is", pearson_coef, " with a P-value of P =", p_value)  