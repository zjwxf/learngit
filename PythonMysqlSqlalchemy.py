'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 
import pymysql

engine_ts = create_engine('mysql+pymysql://tushare:pass@localhost:3306/stocks?charset=utf8&use_unicode=1')
#'mysql+pymysql://tushare:pass@localhost:3306/stocks?charset=utf8'

def read_data():
    sql = """SELECT * FROM stock_basic LIMIT 20"""
    df = pd.read_sql_query(sql, engine_ts)
    return df


def write_data(df):
    res = df.to_sql('stock_basic', engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)


def get_data():
    pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    df = pro.stock_basic()
    return df
 

if __name__ == '__main__':
    df = read_data()
    df = get_data()
    write_data(df)
    print(df)
