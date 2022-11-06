import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/FinalModule_Coursera/data/loan_train.csv')

#df['due_date'] = pd.to_datetime(df['due_date'])
#df['effective_date'] = pd.to_datetime(df['effective_date'])
print(df.head())
print(df['loan_status'].value_counts())
#print(df.hist(column='pricipal', bins=50))
print(df.columns)

X = df[['Unnamed: 0', 'Unnamed: 0.1','Principal','terms','effective_date','due_date','age',	'education','Gender']] .values  #.astype(float)
X[0:5]
y = df['loan_status'].values
y[0:5]
X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))
X[0:5]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)