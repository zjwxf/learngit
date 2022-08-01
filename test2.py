[1mdiff --git a/BacktraderStudy.py b/BacktraderStudy.py[m
[1mindex 5894b61..5e4d06c 100644[m
[1m--- a/BacktraderStudy.py[m
[1m+++ b/BacktraderStudy.py[m
[36m@@ -3,10 +3,11 @@[m [mimport backtrader as bt[m
 import backtrader.feeds as btfeeds[m
 class SmaCross(bt.SignalStrategy):[m
     def __init__(self):[m
[31m-        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)[m
[32m+[m[32m        sma1, sma2 = bt.ind.SMA(period=5), bt.ind.SMA(period=50)[m
         crossover = bt.ind.CrossOver(sma1, sma2)[m
         self.signal_add(bt.SIGNAL_LONG, crossover)[m
 cerebro = bt.Cerebro()[m
[32m+[m[32mcerebro.broker.setcash(200000.0) # set the money[m
 cerebro.addstrategy(SmaCross)[m
 data = btfeeds.GenericCSVData([m
     dataname='stock_data.csv',[m
[36m@@ -17,7 +18,7 @@[m [mdata = btfeeds.GenericCSVData([m
     datetime=1,[m
     open=2,[m
     high=3,[m
[31m-    low=4,    [m
[32m+[m[32m    low=4,[m
     close=5,[m
     volume=9,[m
     openinterest=-1[m
[36m@@ -26,7 +27,14 @@[m [mcerebro.adddata(data)[m
 cerebro.run()[m
 cerebro.plot(iplot=False)[m
 [m
[32m+[m[32m# Print out the starting conditions[m
[32m+[m[32mprint('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
 [m
[32m+[m[32m# Run over everything[m
[32m+[m[32mcerebro.run()[m
[32m+[m
[32m+[m[32m# Print out the final result[m
[32m+[m[32mprint('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
 [m
 [m
 [m
[1mdiff --git a/BacktraderStudy2.py b/BacktraderStudy2.py[m
[1mindex 97f603a..edb1e7d 100644[m
[1m--- a/BacktraderStudy2.py[m
[1m+++ b/BacktraderStudy2.py[m
[36m@@ -43,7 +43,7 @@[m [mclass Teststrategy(bt.Strategy):[m
             #0<-1<-2 close price go down for sequentially for 3 days[m
             if self.dataclose[0]<self.dataclose[-1]:[m
                 if self.dataclose[-1]<self.dataclose[-2]:[m
[31m-                    self.log('BUY CREATE, %2f.' % self.dataclose[0])[m
[32m+[m[32m                    self.log('BUY CREATE, %.2f' % self.dataclose[0])[m
                     self.order =self.buy() #buy for which price?[m
         else:[m
             if len(self) >= (self.bar_executed + 5):[m
[1mdiff --git a/BacktraderStudy6optimizer.py b/BacktraderStudy6optimizer.py[m
[1mindex dce8f8b..acd7c4b 100644[m
[1m--- a/BacktraderStudy6optimizer.py[m
[1m+++ b/BacktraderStudy6optimizer.py[m
[36m@@ -5,7 +5,7 @@[m [mimport os[m
 import backtrader.feeds as btfeeds[m
 [m
 [m
[31m-"""class TestStrategy(bt.Strategy):[m
[32m+[m[32mclass TestStrategy(bt.Strategy):[m
     params=(('maperiod',None),('printlog',False))[m
     def log(self,txt,dt=None,doprint=False):[m
         if self.params.printlog or doprint:[m
[1mdiff --git a/BacktraderStudy7Memory.py b/BacktraderStudy7Memory.py[m
[1mindex 318a2d5..b073cd4 100644[m
[1m--- a/BacktraderStudy7Memory.py[m
[1m+++ b/BacktraderStudy7Memory.py[m
[36m@@ -15,7 +15,7 @@[m [mclass TestInd(bt.Indicator):[m
 [m
     def __init__(self):[m
         self.lines.a = b = self.data.close - self.data.high[m
[31m-        self.lines.b = btind.SMA(b, period=20)[m
[32m+[m[32m        self.lines.b = btind.SMA(b, period=100)[m
 [m
 [m
 class St(bt.Strategy):[m
[36m@@ -29,6 +29,7 @@[m [mclass St(bt.Strategy):[m
         btind.Stochastic()[m
         btind.RSI()[m
         btind.MACD()[m
[32m+[m[32m        btind.BollingerBands()[m
         btind.CCI()[m
         TestInd().plotinfo.plot = False[m
 [m
[36m@@ -126,7 +127,7 @@[m [mdef runstrat():[m
     cerebro.run(runonce=False, exactbars=args.save)[m
     if args.plot:[m
         cerebro.plot(style='bar')[m
[31m-[m
[32m+[m[32m    cerebro.plot(iplot=True)[m
 [m
 def parse_args():[m
     parser = argparse.ArgumentParser([m
[36m@@ -153,4 +154,4 @@[m [mdef parse_args():[m
 [m
 [m
 if __name__ == '__main__':[m
[31m-    runstrat()[m
\ No newline at end of file[m
[32m+[m[32m    runstrat()[m
[1mdiff --git a/bt.stratgy.py b/bt.stratgy.py[m
[1mindex e69de29..9d387d0 100644[m
[1m--- a/bt.stratgy.py[m
[1m+++ b/bt.stratgy.py[m
[36m@@ -0,0 +1,47 @@[m
[32m+[m[32mimport backtrader as bt[m
[32m+[m[32mfrom datetime import datetime[m
[32m+[m
[32m+[m[32mclass TestStrategy(bt.Strategy):[m
[32m+[m
[32m+[m[32m    def log(self, txt, dt=None):[m
[32m+[m[32m        ''' Logging function for this strategy'''[m
[32m+[m[32m        dt = dt or self.datas[0].datetime.date(0)[m
[32m+[m[32m        print('%s, %s' % (dt.isoformat(), txt))[m
[32m+[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        # Keep a reference to the "close" line in the data[0] dataseries[m
[32m+[m[32m        self.dataclose = self.datas[0].close[m
[32m+[m
[32m+[m[32m    def next(self):[m
[32m+[m[32m        pass[m
[32m+[m
[32m+[m[32m        if __name__ == '__main__' :[m
[32m+[m[32m            cerebro = bt.Cerebro()[m
[32m+[m[32m            cerebro.broker.setcash(100000.0)[m
[32m+[m[32m            print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m[32m            cerebro.run()[m
[32m+[m[32m            print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m[32m            cerebro.broker.setcommission(0.002)[m
[32m+[m[32m            #cerebro.addsizer(bt.sizes.FixedSize,stake=100)[m
[32m+[m[32m            data=bt.feeds.GenericCSVData([m
[32m+[m[32m                dataname="stock_data.csv",[m
[32m+[m[32m                datetime=1,[m
[32m+[m[32m                open=2,[m
[32m+[m[32m                high=3,[m
[32m+[m[32m                low=4,[m
[32m+[m[32m                close=5,[m
[32m+[m[32m                volume=9,[m
[32m+[m[32m                dtformat=('%Y%m%d'),[m
[32m+[m[32m                fromdate=datetime(2011,1,1),[m
[32m+[m[32m                todate=datetime(2011,12,31)[m
[32m+[m[32m                    )[m
[32m+[m
[32m+[m[32m        cerebro.adddata(data)[m
[32m+[m[32m        # Print out the starting conditions[m
[32m+[m[32m        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m
[32m+[m[32m        # Run over everything[m
[32m+[m[32m        cerebro.run()[m
[32m+[m
[32m+[m[32m        # Print out the final result[m
[32m+[m[32m        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
\ No newline at end of file[m
[1mdiff --git a/bt.tushare.py b/bt.tushare.py[m
[1mindex 3953fb6..03b3db6 100644[m
[1m--- a/bt.tushare.py[m
[1m+++ b/bt.tushare.py[m
[36m@@ -1,59 +1,67 @@[m
[31m-from __future__ import (absolute_import, division, print_function,[m
[31m-                        unicode_literals)[m
[31m-[m
[32m+[m[32mimport backtrader as bt[m
 from datetime import datetime[m
[31m-import os.path  # To manage paths[m
[31m-import sys  # To find out the script name (in argv[0])[m
 [m
[31m-# Import the backtrader platform[m
[31m-import backtrader as bt[m
[31m-import tushare as ts[m
[31m-import pandas as pd[m
[31m-[m
[31m-if __name__ == '__main__':[m
[31m-[m
[31m-    pro = ts.pro_api([m
[31m-        token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')[m
[31m-    df = pro.daily(ts_code='000001.SZ', start_date='20110101',[m
[31m-                   end_date='20210101').iloc[::-1][m
[31m-    df.to_csv('stock_data.csv', index=False)[m
[31m-    [m
[31m-    [m
[31m-    # Create a cerebro entity[m
[31m-    cerebro = bt.Cerebro()[m
[31m-[m
[31m-    # Datas are in a subfolder of the samples. Need to find where the script is[m
[31m-    # because it could have been called from anywhere[m
[31m-    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))[m
[31m-    datapath = os.path.join(modpath, 'stock_data.csv')[m
[31m-[m
[31m-    # Create a Data Feed[m
[31m-    data = bt.feeds.GenericCSVData([m
[31m-        dataname=datapath,[m
[31m-        fromdate=datetime(2011, 1, 1),[m
[31m-        todate=datetime(2012, 12, 31),[m
[31m-        nullvalue=0.0,[m
[31m-        dtformat=('%Y%m%d'),[m
[31m-        datetime=1,[m
[31m-        open=2,[m
[31m-        high=3,[m
[31m-        low=4,    [m
[31m-        close=5,[m
[31m-        volume=9,[m
[31m-        openinterest=-1[m
[31m-    )[m
[31m-[m
[31m-    # Add the Data Feed to Cerebro[m
[31m-    cerebro.adddata(data)[m
[31m-[m
[31m-    # Set our desired cash start[m
[31m-    cerebro.broker.setcash(300000.0)[m
[31m-[m
[31m-    # Print out the starting conditions[m
[31m-    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[31m-[m
[31m-    # Run over everything[m
[31m-    cerebro.run()[m
[31m-[m
[31m-    # Print out the final result[m
[31m-    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
\ No newline at end of file[m
[32m+[m
[32m+[m[32mclass TestStrategy(bt.Strategy):[m
[32m+[m
[32m+[m[32m    def log(self, txt, dt=None):[m
[32m+[m[32m        ''' Logging function for this strategy'''[m
[32m+[m[32m        dt = dt or self.datas[0].datetime.date(0)[m
[32m+[m[32m        print('%s, %s' % (dt.isoformat(), txt))[m
[32m+[m
[32m+[m[32m    def __init__(self):[m
[32m+[m[32m        # Keep a reference to the "close" line in the data[0] dataseries[m
[32m+[m[32m        self.dataclose = self.datas[0].close[m
[32m+[m
[32m+[m[32m    def next(self):[m
[32m+[m[32m     if __name__ == '__main__':[m
[32m+[m[32m        cerebro = bt.Cerebro()[m
[32m+[m[32m        cerebro.broker.setcash(100000.0)[m
[32m+[m[32m        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m[32m        cerebro.run()[m
[32m+[m[32m        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m[32m        cerebro.broker.setcommission(0.002)[m
[32m+[m[32m        #cerebro.addsizer(bt.sizes.FixedSize,stake=100)[m
[32m+[m[32m        data=bt.feeds.GenericCSVData([m
[32m+[m[32m            dataname="stock_data.csv",[m
[32m+[m[32m            datetime=1,[m
[32m+[m[32m            open=2,[m
[32m+[m[32m            high=3,[m
[32m+[m[32m            low=4,[m
[32m+[m[32m            close=5,[m
[32m+[m[32m            volume=9,[m
[32m+[m[32m            dtformat=('%Y%m%d'),[m
[32m+[m[32m            fromdate=datetime(2011,1,1),[m
[32m+[m[32m            todate=datetime(2011,12,31)[m
[32m+[m[32m                )[m
[32m+[m
[32m+[m[32m"""class TestStrategy(bt.Strategy):[m
[32m+[m[32m    def next(self):[m
[32m+[m[32m        self.log('close,%.2f' % self.dataclose[0])[m
[32m+[m[32m        if self.order:[m
[32m+[m[32m            return[m
[32m+[m[32m        if not self.position:[m
[32m+[m[32m            if self.sma5[0]>self.sma10[0]:[m
[32m+[m[32m                self.log('BUY CREATE,%.2f')[m
[32m+[m[32m                self.order =self.buy()[m
[32m+[m[32m        else:[m
[32m+[m[32m            if self.sma5[5]<self.sma10[10]:[m
[32m+[m[32m                self.log('SELL CREATE,%.2f' %self.dataclose[10])[m
[32m+[m[32m                self.order=self.sell()[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32m    def log(self,txt,dt=None,doprint=False):[m
[32m+[m[32m        if doprint:[m
[32m+[m[32m            dt = dt or self.datas[0].datetime(0)[m
[32m+[m[32m            print('%s,%s' %(dt.isoformat(),txt))"""[m
[32m+[m[32mcerebro.adddata(data)[m
[32m+[m[32m# Print out the starting conditions[m
[32m+[m[32mprint('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[32m+[m
[32m+[m[32m# Run over everything[m
[32m+[m[32mcerebro.run()[m
[32m+[m
[32m+[m[32m# Print out the final result[m
[32m+[m[32mprint('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
\ No newline at end of file[m
[1mdiff --git a/test.py b/test.py[m
[1mdeleted file mode 100644[m
[1mindex 140b6a3..0000000[m
[1m--- a/test.py[m
[1m+++ /dev/null[m
[36m@@ -1,178 +0,0 @@[m
[31m-"""x=(1,2,3,4,5,6,7,8,9)[m
[31m-y=min(x)[m
[31m-u=max(x)[m
[31m-print(y,u)"""[m
[31m-[m
[31m-from __future__ import (absolute_import, division, print_function,[m
[31m-                        unicode_literals)[m
[31m-                    [m
[31m-from ctypes.wintypes import SIZE[m
[31m-from re import A, X[m
[31m-from backtrader.indicators  import Indicator, Max, Min, MovAv,AverageTrueRange,TrueRange[m
[31m-[m
[31m-import backtrader.indicators as btind [m
[31m-import datetime  # For datetime objects[m
[31m-from datetime import datetime #tushare [m
[31m-import backtrader as bt[m
[31m-import backtrader.feeds as btfeeds[m
[31m-import sys[m
[31m-import backtrader.indicators as btind[m
[31m-import numpy as np[m
[31m-[m
[31m-[m
[31m-class TurtleStrategy(bt.Strategy): [m
[31m-    params = ( ('mpperiod1',20), ('mpperiod2',5), ('movav', MovAv.Smoothed))[m
[31m-    alias = ('ATR',)[m
[31m-    lines = ('atr',)[m
[31m-    def log(self, txt, dt=None):[m
[31m-        dt = dt or self.datas[0].datetime.date(0)[m
[31m-        #print('%s, %s' % (dt.isoformat(), txt))[m
[31m-[m
[31m-[m
[31m-    def __init__(self):[m
[31m-        self.dataclose = self.data.close[m
[31m-        self.datahigh = self.data.high[m
[31m-        self.datalow =self.data.low[m
[31m-        self.dataopen =self.data.open[m
[31m-        self.datahigMax = Max(self.datahigh)[m
[31m-        print(self.datahigMax)[m
[31m-        [m
[31m-        self.order = None[m
[31m-        self.buyprice = None[m
[31m-        self.buycomm = None[m
[31m-        self.lines.tr = bt.indicators.TrueHigh(self.data) - bt.indicators.TrueLow(self.data)[m
[31m-        [m
[31m-[m
[31m-        self.atr1 = bt.indicators.AverageTrueRange(self.datas[0], period=self.params.mpperiod1)[m
[31m-        self.atr2 = bt.indicators.AverageTrueRange(self.datas[0], period=self.params.mpperiod2)[m
[31m-        #self.sell_sig = min(self.datas.close[-10,0])[m
[31m-        #print(self.atr1[0])[m
[31m-        [m
[31m-[m
[31m-        self.lines.atr = self.p.movav(bt.indicators.TrueRange(self.data), period=self.p.mpperiod1)[m
[31m-        #self.buy_sig =bt.And()[m
[31m-        list = min(self.data.close[0],self.data.close[-1],self.data.close[-2])[m
[31m-        list2 =max(self.data.close[0],self.data.close[-1],self.data.close[-2])[m
[31m-        list3 = (self.data.close[0],self.data.close[-1],self.data.close[-2])[m
[31m-        max_value= max(list3)[m
[31m-[m
[31m-        #print(max_value)[m
[31m-        #print(max(list3), 'list3,ok')[m
[31m-        #print(list)[m
[31m-        #print(list2,'ok')[m
[31m-        #print(list3,'list3 ok')[m
[31m-        #self.list_atr1 = list.append(self.atr1)[m
[31m-        #生成一个atr1的数列 ，周期用params控制[m
[31m-[m
[31m-        i = 0[m
[31m-        list4=[][m
[31m-        list_LowMin=[None]*21[m
[31m-        list_highMax =[None]*21[m
[31m-        for i in range(-21,0):[m
[31m-            #print('i Range(1,10)', 'i=',i)[m
[31m-            list_LowMin[i]=self.dataclose[i][m
[31m-            list_highMax[i]=self.datahigh[i][m
[31m-            print('list_LowMax[i]',list_LowMin)[m
[31m-            #print('self.dataclose[0]',self.dataclose[0])[m
[31m-        print('list_lowMin=', list_LowMin)[m
[31m-        self.Result_lowMin=min(list_LowMin)[m
[31m-        self.Result_highMax=max(list_highMax)[m
[31m-        print('Result_lowMin',self.Result_lowMin)[m
[31m-        print('Result_highMax',self.Result_highMax)[m
[31m-        #Result_max_list4=list4.extend(list_LowMax)[m
[31m-        #print('Result_max_list4',Result_max_list4)[m
[31m-[m
[31m-[m
[31m-        """b=max(list_LowMax[i])[m
[31m-            print(b,'b is ok')[m
[31m-            list4=[list_LowMax][m
[31m-            print('list4',list4)[m
[31m-            list4.append(list_LowMax)[m
[31m-            print(list4)"""[m
[31m-[m
[31m-    def notify_order(self,order):[m
[31m-        if order.status in [order.Submitted,order.Accepted]:[m
[31m-            return [m
[31m-        if order.status in [order.Completed]:[m
[31m-            if order.isbuy():[m
[31m-                self.log([m
[31m-                    'BUY EXECUTED,ref:%.0f,Stock:%s Price:%.2f, Cost:%.2f, Commmision %.2f, Size%.2f,' %[m
[31m-                        (order.ref,[m
[31m-                        order.data._name,[m
[31m-                        order.executed.price,[m
[31m-                        order.executed.value,[m
[31m-                        order.executed.comm,[m
[31m-                        order.executed.size,[m
[31m-                        ))[m
[31m-                self.buyprice = order.executed.price[m
[31m-                self.buycomm = order.executed.comm[m
[31m-            else:#sell[m
[31m-                self.log('SELL EXECUTED, ref:%.0f, Stock:%s, Price:%.2f, Cost:%.2f,commision:%.2f,Size%.2f'%[m
[31m-                   (order.ref,[m
[31m-                   order.data._name,[m
[31m-                    order.executed.price,[m
[31m-                    order.executed.value,[m
[31m-                    order.executed.comm,[m
[31m-                    order.executed.size[m
[31m-                    ))[m
[31m-                self.bar_executed = len(self)[m
[31m-[m
[31m-        elif order.status in [order.Canceled,order.Margin,order.Rejected]:[m
[31m-            self.log('Order Canceled/Margin/Rejected')[m
[31m-        self.order =None[m
[31m-[m
[31m-    def notify_trade(self, trade):[m
[31m-        if not trade.isclosed:[m
[31m-            return[m
[31m-        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %[m
[31m-                (trade.pnl, trade.pnlcomm)[m
[31m-                )[m
[31m-[m
[31m-    def next(self):[m
[31m-        self.log('Close, %.2f' % self.dataclose[0])[m
[31m-        #print(self.atr1[0])[m
[31m-        #atr1_array=np.insert(self.atr1,self.atr1[0])[m
[31m-        #print('atr1_array, %.2f'% atr1_array)[m
[31m-        if self.order:[m
[31m-            return[m
[31m-        if not self.position:[m
[31m-            if self.dataclose[0]>self.Result_highMax:[m
[31m-                #if self.dataclose[-1]<self.dataclose[-2]:[m
[31m-                self.log('BUY CREATE, %.2f' % self.dataclose[0])[m
[31m-                self.order = self.buy()[m
[31m-        else:[m
[31m-            if self.dataclose[0] < self.atr2[0] or self.dataclose[0]<self.atr1[0]:[m
[31m-                #len(self) >= (self.bar_executed +  self.params.exitbars)[m
[31m-                #self.log('SELL CREATE, %.2f' % self.dataclose[0])[m
[31m-                #keep track of the created order to avoid 2nd order[m
[31m-                self.order = self.sell() [m
[31m-[m
[31m-[m
[31m-[m
[31m-if __name__=='__main__':[m
[31m-    cerebro =bt.Cerebro()[m
[31m-    cerebro.addstrategy(TurtleStrategy)[m
[31m-    data = bt.feeds.GenericCSVData([m
[31m-        dataname= 'stock_data.csv',[m
[31m-        fromdate=datetime(2011, 1, 1),[m
[31m-        todate=datetime(2011, 12, 31),[m
[31m-        nullvalue=0.0,[m
[31m-        dtformat=('%Y%m%d'),[m
[31m-        datetime=1,[m
[31m-        open=2,[m
[31m-        high=3,[m
[31m-        low=4,[m
[31m-        close=5,[m
[31m-        volume=9,[m
[31m-        openinterest=-1,[m
[31m-    )[m
[31m-cerebro.adddata(data)[m
[31m-#self.sizer.setsizing(self.params.stake)[m
[31m-cerebro.addsizer(bt.sizers.FixedSize,stake=100)[m
[31m-cerebro.broker.setcash(100000.0)[m
[31m-cerebro.broker.setcommission(commission=0.001)[m
[31m-print('Starting Protfolio Value: %.2f' % cerebro.broker.getvalue())[m
[31m-cerebro.run()[m
[31m-print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[31m-#cerebro.plot(iplot=None)[m
[31m-[m
[1mdiff --git a/test2.py b/test2.py[m
[1mdeleted file mode 100644[m
[1mindex 4e518c4..0000000[m
[1m--- a/test2.py[m
[1m+++ /dev/null[m
[36m@@ -1,116 +0,0 @@[m
[31m-from __future__ import(absolute_import,division,print_function,unicode_literals)[m
[31m-from datetime import datetime[m
[31m-import backtrader as bt[m
[31m-import backtrader.feeds as btfeeds[m
[31m-import backtrader.indicators as btind[m
[31m-[m
[31m-class TurtleStrategy(bt.Strategy):[m
[31m-    params=(('periopd1', 20), ('period2', 10))[m
[31m-    def log(self,txt,dt=None,doprint=False):[m
[31m-        if self.params.pprintlog or doprint:[m
[31m-           self.dt=dt or self.datas[0].date(0)[m
[31m-           print('%s, %s' %(dt.isoformat()),txt)[m
[31m-    def __init__(self):[m
[31m-        self.dataclose = self.data.close[m
[31m-        self.datahigh = self.data.high[m
[31m-        self.datalow = self.data.low[m
[31m-        #self.atr = bt.ind.TrueHigh[m
[31m-        self.order = None [m
[31m-        self.pprice = None[m
[31m-        self.buyprice = None [m
[31m-[m
[31m-        """"i=0[m
[31m-        for i in range(-3,0):[m
[31m-            list_20_high[i] = self.datahigh[i][m
[31m-        self.max_20_high =max(list_20_high)[m
[31m-        print(self.max_20_high)[m
[31m-        for i in range(-3,0):[m
[31m-            list_10_low[i] = self.datalow[i][m
[31m-        self.min_10_low =min(list_10_low)[m
[31m-        print(self.min_10_low)"""[m
[31m-[m
[31m-    def notify_order(self,order):[m
[31m-        if order.status in [order.Submitted,order.Accepted]:[m
[31m-            return [m
[31m-        if order.status in [order.Completed]:[m
[31m-            if order.isbuy():[m
[31m-                self.log([m
[31m-                    'BUY EXECUTED,ref:%.0f,Stock:%s Price:%.2f, Cost:%.2f, Commmision %.2f, Size%.2f,' %[m
[31m-                        (order.ref,[m
[31m-                        order.data._name,[m
[31m-                        order.executed.price,[m
[31m-                        order.executed.value,[m
[31m-                        order.executed.comm,[m
[31m-                        order.executed.size,[m
[31m-                        ))[m
[31m-                self.buyprice = order.executed.price[m
[31m-                self.buycomm = order.executed.comm[m
[31m-            else:#sell[m
[31m-                self.log('SELL EXECUTED, ref:%.0f, Stock:%s, Price:%.2f, Cost:%.2f,commision:%.2f,Size%.2f'%[m
[31m-                   (order.ref,[m
[31m-                   order.data._name,[m
[31m-                    order.executed.price,[m
[31m-                    order.executed.value,[m
[31m-                    order.executed.comm,[m
[31m-                    order.executed.size[m
[31m-                    ))[m
[31m-            #self.bar_executed = len(self)[m
[31m-[m
[31m-        elif order.status in [order.Canceled,order.Margin,order.Rejected]:[m
[31m-            self.log('Order Canceled/Margin/Rejected')[m
[31m-        self.order =None[m
[31m-    def notify_trade(self, trade):[m
[31m-        if not trade.isclosed:[m
[31m-            return[m
[31m-        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %[m
[31m-                (trade.pnl, trade.pnlcomm)[m
[31m-                )[m
[31m-    def _next(self):[m
[31m-        self.log('Close,%2f.' %self.dataclose[0])[m
[31m-        list_20_high=[None]*3[m
[31m-        list_10_low=[None]*3[m
[31m-        i=0[m
[31m-        for i in range(-3,0):[m
[31m-            list_20_high[i] = self.datahigh[i][m
[31m-        self.max_20_high =max(list_20_high)[m
[31m-        print(self.max_20_high)[m
[31m-        for i in range(-3,0):[m
[31m-            list_10_low[i] = self.datalow[i][m
[31m-        self.min_10_low =min(list_10_low)[m
[31m-        print(self.min_10_low)[m
[31m-        if self.order:[m
[31m-            return[m
[31m-        if not self.position:           [m
[31m-            if self.dataclose[0] > self.max_20_high:[m
[31m-                self.log('BUY CREATE, %.2f' % self.dataclose[0])[m
[31m-                self.order = self.buy()[m
[31m-            if self.dataclose[0] > self.max_20_high:[m
[31m-                self.log('SELL CREATE, %.2f' % self.dataclose[0])[m
[31m-                self.order = self.sell()[m
[31m-            [m
[31m-if __name__=='__main__':[m
[31m-    cerebro =bt.Cerebro()[m
[31m-    cerebro.addstrategy(TurtleStrategy)[m
[31m-    data = bt.feeds.GenericCSVData([m
[31m-        dataname= 'stock_data.csv',[m
[31m-        fromdate=datetime(2011, 1, 1),[m
[31m-        todate=datetime(2011, 12, 31),[m
[31m-        nullvalue=0.0,[m
[31m-        dtformat=('%Y%m%d'),[m
[31m-        datetime=1,[m
[31m-        open=2,[m
[31m-        high=3,[m
[31m-        low=4,[m
[31m-        close=5,[m
[31m-        volume=9,[m
[31m-        openinterest=-1,[m
[31m-    )[m
[31m-cerebro.adddata(data)[m
[31m-#self.sizer.setsizing(self.params.stake)[m
[31m-cerebro.addsizer(bt.sizers.FixedSize,stake=100)[m
[31m-cerebro.broker.setcash(100000.0)[m
[31m-cerebro.broker.setcommission(commission=0.001)[m
[31m-print('Starting Protfolio Value: %.2f' % cerebro.broker.getvalue())[m
[31m-cerebro.run()[m
[31m-print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())[m
[31m-#cerebro.plot(iplot=None)[m
[1mdiff --git a/tusharegetdata.py b/tusharegetdata.py[m
[1mindex d7bd1ea..960005e 100644[m
[1m--- a/tusharegetdata.py[m
[1m+++ b/tusharegetdata.py[m
[36m@@ -5,6 +5,3 @@[m [mpro = ts.pro_api([m
 df = pro.daily(ts_code='000001.SZ', start_date='20110101',[m
                end_date='20210101').iloc[::-1][m
 df.to_csv('stock_data.csv', index=False)[m
[31m-[m
[31m-[m
[31m-[m
