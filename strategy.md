# analysis

markdown

## system 1

### factor N

TR = max(H-L, abs(H-C(-1)), abs(C(-1)-L))

ATR(x) = avg(TR[x])

N = (19*N(-1)+TR0)/20

* N(ini) = ATR(20)

### initial volume

PV = price unit value (i.e. Cu, Vmin=5, PV=5)

EQi = initial equity (i.e. 1m)

Vi = initial volume

EQi/100=PV*N*Vi

Vi = EQi/100/PV/N (i.e. 1m/100/5/N=?)

### break price

Long: Px > H(x-20)

Short: Px < L(x-20)

if position is 0, any break price is valid to open position

otherwise, break price should be ignored

### increase position

once position opened, increase position every N/2

### stop loss

SL = latest open - 2N (apply to all position)

### take profit

Long: TP = Px < L(x-10)

Short: TP = Px > H(x-10)


### 文档BacktraderTuschareDateFeed.py 导入了tushare数据到Backtrader

2022.09.01
1.use of df to filter 21days(variable) first new high for buy
  1.1.1 21days(variable) for sell (finish,problem no data  index out of range)
  1.1.2 find the lowest buy position with double lines or triple lines (sma)
  1.1.3 double sma cross using Tushare df
  1.2.1 backtrader double sma cross (1.pd.to_datetime ,datetime.now() detla=datetime.timedetal(360days), data = data[data['list_date'] < (now- delta)])

2.milestone finish datafeed from  Tushare to backtrader import
3.backtrader Turtlestratgie with multi parameters
4.pyfolio under plt.Show() works with diagrm but not results conclusion, in jupterbook the schema of results works but not the diagram
  BacktraderTushareDataFeed.py  plt.show()  show the diagram but not table of statistic
  in jupterbook:
  pf.create_simple_tear_sheet(returns,
                             positions=None,
                             transactions=None,
                             benchmark_rets=None,
                             slippage=None,
                             estimate_intraday='infer',
                             live_start_date= None,
                             turnover_denom='AGB',
                             header_rows=None)
 'simple' methode works good

5.results of analysis to dataframe(result yes=0 no =1), on AI to find out the sussecce rate of the methode/strategie
 5.1.1 Highst/lowest point break signal ,relasionship with : days of up/down, volatility, MACD, RSI,KSI, PE ,PB PE/PB 
