import backtrader as bt
from datetime import datetime

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        pass

        if __name__ == '__main__' :
            cerebro = bt.Cerebro()
            cerebro.broker.setcash(100000.0)
            print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
            cerebro.run()
            print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
            cerebro.broker.setcommission(0.002)
            #cerebro.addsizer(bt.sizes.FixedSize,stake=100)
            data=bt.feeds.GenericCSVData(
                dataname="stock_data.csv",
                datetime=1,
                open=2,
                high=3,
                low=4,
                close=5,
                volume=9,
                dtformat=('%Y%m%d'),
                fromdate=datetime(2011,1,1),
                todate=datetime(2011,12,31)
                    )

        cerebro.adddata(data)
        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        # Run over everything
        cerebro.run()

        # Print out the final result
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())