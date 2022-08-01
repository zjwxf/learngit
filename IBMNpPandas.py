
print("hello Mike".find("Mike"))
print(int(False))
print('1'+'2' )
print('hello'.upper())
print( str(1)+str(1))
#print(type(x=1/1))
x=1/1
print(x)
B=[1,2,[3,'a'],[4,'b']]
print(B[2][0])
print([1,2,3]+[1,1,1])
A = [1]
A.append([2,3,4,5])
print(A)
b=len(A)
print(b)
print("HelloMike".split())
Dict={"A":1,"B":"2","C":[3,3,3],"D":(4,4,4),'E':5,'F':6}
print(Dict["D"])
print(Dict["A"])
c={"A","A"}
print(c)

d=set([1,2,3])
print(type(d))
print( {'a','b'} &{'a'})
A=((11,12),[21,22])
print(A[1])

A=((1),[2,3],[4])
print(A[[2][0]])
L=[1,2,3]
L.append(['a','b'])
e=len(L)
print(e)
print(L)

A=[1,2,4,5,6,7,8]
B=A[:]
print(B)
l= len(("disco",10))
print(l) 

a={ "The Bodyguard":"1992", "Saturday Night Fever":"1977"}
b=a.values()
c=a.keys()
print(b,c)

V={'1','2'}
V.add('3')
print(V)

print("1=2")

for i in range(0,3):
    print(i)
for i,x in enumerate(["a","b","c"]):
    print(i,x)



def Mult(a, b):
    c = a * b
    return(c)    
result = Mult(12,2)
print(result)


myFavouriteBand = "AC/DC"
def getBandRating(bandname):
    myFavouriteBand = "Deep Purple"
    if bandname == myFavouriteBand:
        return 10.0
    else:
        return 0.0
print("AC/DC's rating is:",getBandRating("AC/DC"))
print("Deep Purple's rating is: ",getBandRating("Deep Purple"))
print("My favourite band is:",myFavouriteBand)


x=5
while(x!=2):
  print(x)
  x=x-1

a=1

def do(x):
    a=100
    return(x+a)

print(do(1))


import pandas as pd

x = {'Name': ['Rose','John', 'Jane', 'Mary'], 'ID': [1, 2, 3, 4], 'Department': ['Architect Group', 'Software Group', 'Design Team', 'Infrastructure'], 
      'Salary':[100000, 80000, 50000, 60000]}
#casting the dictionary to a DataFrame
df = pd.DataFrame(x)
df.head()
#display the result df
print(df)
"""print(df.loc[0,'Salary'])
print(df.iloc[0,0])
print(df.iloc[[0]])
print(df.iloc[0])
print(df.loc[1:3,'Name':'Salary'])
print(df.iloc[0:4,0:4])"""
print(df.iloc[1,1])
print(df.loc[1,'ID'])

df1=df.set_index('Name')
print(df1.loc['John','ID'])
print(df.describe)
print(df.info)
print(df.isnull())
print(df.notnull())
for column in df.columns.values.tolist():
    print(column)
    print(df[column].value_counts())
#print(df1)



import numpy as np
b = np.array([3.1, 11.02, 6.2, 213.2, 5.2])
# Enter your code here
print(type(b))
print(b.dtype)
b[1]=100
c=list(b)
print(c)
print(b)

arr = np.array([1, 2, 3, 4, 5, 6, 7])
print(arr[1:5:1])
print(arr[:4])
print(arr[4:])
print(arr.size)
print(arr.ndim)
print(arr.shape)
mean=arr.mean()
print(mean)
print(arr.std())
print(arr.max())
print(arr.min())

arr1 = np.array([10, 20, 30, 40, 50, 60])
arr2 = np.array([20, 21, 22, 23, 24, 25])
arr3=np.subtract(arr1,arr2)
print(arr3)



X = np.array([1, 2,3])
Y = np.array([3, 2,1])
print(np.dot(X,Y))
z=np.dot(X, Y)
print(z)
print(X[0])
print(X[1])
print(Y[0])
print(Y[1])



print(np.linspace(-2, 2, num=9))


a=np.array([-1,1])
b=np.array([1,1])
print(np.dot(a,b)) 
print(a*b)
print(np.multiply(a,b))

X=np.array([[1,0,1],[2,2,2]]) 
out=X[0,1:3]
print(out)

X=np.array([[1,0],[0,1]])
Y=np.array([[2,1],[1,2]]) 
print(np.dot(X,Y))

import requests
import os
from PIL import Image
from IPython.display import IFrame
url='http://www.ibm.com'
r= requests.get(url)
print(r.status_code)
print(r.request.headers)
print("request body", r.request.body)
print(r.headers)

"""path=os.path.join(os.getcwd(),'image.png')
with open(path,'wb') as f:
    f.write(r.content)
    Image.open(path)"""

df=pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
print(df)
df = df.transform(func = lambda x : x + 10)
print(df)
print(df.info)
print(df.describe)


import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0.5, 10, 1000)
y = np.cos(x)
plt.plot(x, y, ls='-', lw=2, label='cosine', color='purple')
plt.legend()
plt.xlabel('independent variable')
plt.ylabel('dependent variable')
plt.show()

{
  "apikey": "3T3Itc044a2TBQtp0YME8q3EqXNPhbOiTImFx8icbGYu",
  "iam_apikey_description": "Auto-generated for key crn:v1:bluemix:public:speech-to-text:us-south:a/3b6d7d08dfe2404e89dc945c53f8e56e:630887ec-6adb-4d71-9fcb-6b7ab38d122f:resource-key:c50e1a10-6829-4e3b-83af-07e00b72fadf",
  "iam_apikey_name": "Auto-generated service credentials",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/3b6d7d08dfe2404e89dc945c53f8e56e::serviceid:ServiceId-9637e9b9-ded9-495c-b419-0fad7ecea77b",
  "url": "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/630887ec-6adb-4d71-9fcb-6b7ab38d122f"
}
#speech to text api watson

"""
import time 
import sys
import numpy as np 
import matplotlib.pyplot as plt 
u = np.array([1, 0])
v = np.array([0, 1])
z = np.add(u, v)
def Plotvec1(u, z, v):
    
    ax = plt.axes() # to generate the full window axes
    ax.arrow(0, 0, *u, head_width=0.05, color='r', head_length=0.1)# Add an arrow to the  U Axes with arrow head width 0.05, color red and arrow head length 0.1
    plt.text(*(u + 0.1), 'u')#Adds the text u to the Axes 
    
    ax.arrow(0, 0, *v, head_width=0.05, color='b', head_length=0.1)# Add an arrow to the  v Axes with arrow head width 0.05, color red and arrow head length 0.1
    plt.text(*(v + 0.1), 'v')#Adds the text v to the Axes 
    
    ax.arrow(0, 0, *z, head_width=0.05, head_length=0.1)
    plt.text(*(z + 0.1), 'z')#Adds the text z to the Axes 
    plt.ylim(-2, 2)#set the ylim to bottom(-2), top(2)
    plt.xlim(-2, 2)#set the xlim to left(-2), right(2)
plt(Plotvec1(u,z,v))"""

var = '01234567'
print(var[::2])
print(var.find("2"))
Name="ABCDE"
print(Name.find("C"))
print(2//3)

a='1,2,3,4'
print(a.split(','))



y=df[['Artist','Length','Genre']]
print(y)