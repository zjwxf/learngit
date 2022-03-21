from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import tushare as ts
import pandas as pd

if __name__ == '__main__':

    pro = ts.pro_api(
        token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    df = pro.daily(ts_code='000001.SZ', start_date='20110101',
                   end_date='20210101').iloc[::-1]
    df.to_csv('stock_data.csv', index=False)
    
    
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'stock_data.csv')

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime(2011, 1, 1),
        todate=datetime(2012, 12, 31),
        nullvalue=0.0,
        dtformat=('%Y%m%d'),
        datetime=1,
        open=2,
        high=3,
        low=4,    
        close=5,
        volume=9,
        openinterest=-1
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(300000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())