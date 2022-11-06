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
 5.1.1 Highst/lowest point break signal ,relasionship with : days of up/down, volatility, MACD, RSI,KSI, PE ,PB PE/PB . H/L piont 5/10/20/50/100 days price tredence
 5.1.1.1  Diff = MA5-MA20  if Diff.max(i)  is max df[close][i], diff_pct=100%*(ma5-ma100)/ma100 , diff-pct 不同行业/板块（industry） 波动，峰值（差异大，行业，市值），谷值（比较一致）
          统一数据后pd.melt 增加行业，板块，市值等指标作为参数列


pandas.get_dummies(data, prefix=None, prefix_sep='_', 
			dummy_na=False, columns=None, 
			sparse=False, drop_first=False, dtype=None)
Feature = databasic['industry']
Feature = pd.concat([Feature,pd.get_dummies(databasic['area'])], axis=1) #industry为列，area为行，行业在地区的数量值 
pandas.concat
pandas.melt
df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)  #计算不同gender的loan_status的分类的百分比
df['industry'].value_counts() 计算每种industry的数量
data["gender"] = data["gender"].map({"男":1, "女":0})
df.applymap(lambda x:"%.2f" % x)
# 沿着0轴求和
data[["height","weight","age"]].apply(np.sum, axis=0)  ### axis=o 列  axis=1 行

1.有监督学习中，数据 = (特征，标签)，而其主要任务是分类和回归。
1.1如果预测的是离散值 (discrete value)，例如比赛结果赢或输，此类学习任务称为分类 (classification)
1.2如果预测的是连续值 (continuous value)，例如詹姆斯效率 65.1, 70.3 等等，此类学习任务称为回归 (regression)
2.无监督学习 (unsupervised learning) 是找出输入数据的模式。比如，它可以根据电影的各种特征做聚类，用这种方法收集数据为电影推荐系统提供标签。此外无监督学习还可以降低数据的维度，它可以帮助我们更好的理解数据。
在无监督学习中，数据 = (特征，)。
2.1除了根据詹姆斯个人统计来预测骑士队输赢或者个人效率值外，我们还可以对该数据做聚类 (clustering)，即将训练集中的数据分成若干组，每组成为一个簇 (cluster)
2.2后来发现簇 A 代表赢，簇 B 代表输。聚类的用处就是可以找到一个潜在的原因来解释为什么样例 1 和 3 可以赢球。难道真的是只要詹姆斯三双就可以赢球？

![markdown picture](https://img-blog.csdnimg.cn/img_convert/9fb6b08131ccdaf97a2615f8e97e9ccf.png)

### 如何分析数据--因子的选择--分析的方法？ 经济计量学？？ 截面 ？时序？
计量经济学：
1 多元线性回归： 
1.1估计
1.2推断
1.3渐进
2.时序数据的自相关与异方差


短期反转异象 short-term reversal anomaly A股最显著的异象。（超跌反弹，原因是短期无差别暴跌）
1.1 过去一个月，跌幅最大组= loser ,升幅最大组为Winner，共5组
1.2 （1）基本面恶化（剔除）== T期的现金流变化
 （2）投资者对信息过度反应(业绩预报) 
 （3）市场流动性冲击
1.3独立双重排序 P.208
    指标因子前一个月股价涨跌幅分5组 Loser P2 P3 P4 Winner
    F-Score将股票分三组 Low Middle High
    3X5=15个投资组合
         L     M     H
  L     L/L   L/M    LH
  P2    P2/L  P2/M   P2/H
  p3    P3/L  P3/M   P3/H
  p4    P4/L  P4/M   P4/H
  W     W/L   W/M     W/H

G-Score
moharan(2005)
打分 P198
8个指标  高于行业“中位数”为1分 低于0分
1. 盈利能力指标 ROA CFOA　 ROA－CFOA
2. 保守会计处理 R&D/总资产( R&D(TTM)/总资产(平均))   销售费用(TTM)/总资产(平均)   资本性开支(TTM)/总资产(平均)
3. 盈利稳定性   ROA方差(过去三年"单季度"ROA方差)　　　营收同比增长率方差(过去三年"单季度"同比"增长率"的方差)
得分加总,分三组 L 0-1/ M 2_5/ H 6-8
BM*G独立双重排序 = 3X3矩阵=9个投资组合 等权重-市值权重-- 结论等权重下G高分在3个组别分别明显,可以区分公司质量.市值权重下 G 区分不明显,受小市值影响



预测变量选取
1. 逻辑性
就是寻找预测变量时最重要的 标准。如果没有底层的逻辑，再漂亮的结果都没有灵魂。
2. 持续性
在评价有 效性时，常用的步骤包括：IC测试、投资组合排序法以及发表前后检验等
投资组合排序法是学术界构建并检验异象的常见手段
多重排序、构建投资组合。之后通过时序回归检验该组合能否获 得相对基准模型的超额收益，如果答案是肯定的，那么就称该预测变量有效
3. 增量信息
如果新的变量和已有变量 相关性很低，表明它可能特立独行，因而更有可能提供增量信息
4. 稳健性
稳健性衡量的是预测变量对构造方法或参数是否敏感，以及在不同的实证区 间内表现是否一致。
学术上:12个月的收益率（剔除最近1个月）作为选股的变量
假如将12换成13或是11，如果动量变量在新的参数下表现差异不大， 就说明其稳定性好
划分样本有多种方式，例如可以按10年为窗口划分区间，也可以 按照商业周期划分样本，还可以按变量被发表前后分为样本内和样本外。一个优秀的预测变量在不同区间内的表现虽然存在差异，但总体来看都有不俗的表现。
5. 可投资性
多空,市场容量,流动性
6. 普适性
普适性的变量能够经受起不同 市场的检验


收益率预测
1. 选股
投资范围的确定包括原始股票池和优化股票池两步
黑名单的来源上，可以分成三类：低流动性股票、高风险
2. 剔除预测变量异常值
量在股票截面上的异常值进行处理。这么做 的目的一方面是为了排除数据错误，另一方面让数据的分布更加均匀。剔除异常 值的方法较多，常见的有缩尾法、三倍标准差法和中位数法。
3. 非参数化预测
  首先来看非参数化预测的方法，包括条件选股和排序打分两种
  由于这两种 法对于变量和收益率之间的具体关系不做假设，而仅是利用二者之间的单调相关性，故而称为非参数法
  以BM和ROE（TTM）为变量条件选股的累计收益率 条件选股法简单直接，许多传奇基金经理的选股方法均可描述成条件选股[7]
  条件法:
  第一，选股条件不能过多或 过少。若条件太多，满足所有条件的股票可能很少甚至不存在；若条件太少，筛 选出来的股票又太多，对资金少的投资者来说会在交易层面造成困难。
  第二，条 件选股往往造成持股数量在时序上非常不稳定。
  第三，由于需要给每个预测变量 设置一个阈值，因此发生过拟合的可能性较高。
  第四，非参数化的条件选股结果 往往难以和投资组合优化模型相融合，因而无法实施更精确的组合管理和风险控制。
  排序打分法:
  在该方法中，使用每个预测变量分 别对每只股票排序，排序时遵循“排名和预期收益正相关”的原则，因此排名靠前的股票得分高，未来预期收益率也更高。
  按照每个变量排序后，将所有变量上的得分加总便得到股票的总分，并从中选出总分最高的N支。
  依然以BM和 ROE（TTM）为预测变量，在每月月末选择总分最高的50支股票等权重配置。
  优点:它能同时考虑多个指标，且选股数量能够保证稳定和可控，参数过度拟合嫌疑也更低。
  缺点:是基础的排序打分法假定每个变量的权重相同，不考虑预测变量预测能力的差异以及预测能力的变化。
  同样的问题在条件选股法中也依然存在。确定预测变量之间的权重属于因子择时的范畴.(定投可以视为解决择时的一种方法)

  参数化预测 Z-Score    P302
  1. 线性回归模型也常被用于收益率的预测。
  在线性回归模型中，"解释变量"是"预测变量"，而"被解释变量"则是"股票收益率"。
  由于不同的预测 变量量纲不统一（比如BM和对数市值），因此通常先对每个预测变量进行标准化处理，得到标准化得分。该得分通常被称为Z-Score[8]
  2. Z-Score= (变量-变量均值)/变量标准差
     变量均值和变量标准差均使用t期股票池中的所有股票在该变量上的取值计算，因而是截面统计量
     回归:
     第一种方式是将所有变量加总，使每支股票得到一个综合得分，然后用该综合得分作为解释变量并通过一元回归来预测收益率。
     第二种方式则是将不同的变量视 作多个解释变量，通过多元回归来预测收益率。

     一元回归:   P303
     为进行一元回归，首先需要得到股票在全部预测变量上的综合得分。为此， 将每个变量的Z-Score按某个权重求和即可(理论上，变量的权重应和它们预测未来收益率的能力成正 比。然而在实践中，等权重配置所有变量往往就是很好的选择)
     综合Z-Score= 加总(Z*每个变量的权重K)
     需要说明的是，按照 式（ 7.4）计算出来的t期每支股票的"综合Z-Score"虽然仍然满足截面均值为0（因为 每个单一的Z-Scorek的均值都是0），但其截面标准差通常不再为1，而是小于1。 因此，需要对式（ 7.4）计算出的综合Z-Score最后再进行一次标准化处理，使得其截面标准差为1.
     下一 元截面回归模型： Rit=ct+btzit−1+εit, i=1, ···, N （ 7.5） 式中zit−1表示t-1时刻（即t期期初）股票i的综合Z-Score。



     2022.10.12
     1. Ma-Diff-Pct 在指数上成功运行，下一个目标是EMA 5-20 5-100
     2. 整理当期py作API, 首先Tushare数据引入，处理为BT格式，输入不同的目标（或全部目标），周期/参数的修改， Size仓位控制(PrecentSizer, AllInSizer,FixSizer)加建仓，
     3. 仓位控制教材（finished),注意原文使用的EMA为ATR技术基础，本PY使用的是SMA，待改进------！！！！！！（finish）
        2022.10.26 回测中SMA的收益及交易机会均优于EMA
        　　　　　　仓位，对于左侧MADIFFPCT模型AllInSizer最优，逻辑上也是（信号90%情况就是市场的底部的90%位置），唯有信号失真(牛市高位下跌才会失真)，融资仓可以解决后续补仓的问题
                    仓位，右侧Turtle 大部分情况下Buysize= 0.01value/N 是最优参数，逻辑上第一仓是最底仓成本最低。
     2022.1018
     1. BacktraderTurtleClean.py 是一个参数优化的BT实例，cerebro.optstrategy(TurtleStrategy,long_period=long_list,short_period=short_list) ，比较不同周期的ATR H/L -line回测优化。finish
     2. AppTushareDiffPctDataframe.py 是一个画图实例， 价格图 和 指标图共轴显示，方便判断策略执行与图表关系
     3. BacktraderTurtlLongOnly.py 是对BacktraderTurtleClean.py按照海龟原文优化的回测实例，优化：（1）定义了N （2）N初始为常熟，用于加仓计算以及初始仓位计算，初始/加仓仓位为常数=资金*1%/（N*（乘以合约点值）），cerebro.addsizer()仓位管理执行器
     4. BacktraderTurtleShortOnly.py 是在BacktraderLongOnly.py基础上做的逆向，实际回测效果不佳，猜测short的全线逻辑或参数与long的分别较大，待改进------！！！！！！
     5. 画图唐安琪通道与价格图共轴 ，暂停，优先级==3
     6. 全面回测报告API ？？？？？？？？/ 优先级=2
     7. 优先级==1 把海龟的仓位控制方法用于MADiffPCT指标上，
        问题：BacktraderTurtleLongOnly.py 初始仓位计算1000000*0.01=10000 　size＝10000/ATR(20) 得到的数值经常导致无法开仓
              self.buy_size = int(self.broker.getvalue() / self.data.close)*0.2 固定仓位 最大5仓。

     2022.10.22
     1. MaDiffPct 左侧交易，追跌不追涨
      (1) 交易标的 000001.SH，399001.SZ ,399006.SZ,000688SH
     （1）T[-1]-13%,T[0]买入，所有买入点均非该次机会的最优秀买点，因此买入策略， T[0]买入70%（融资）仓位，每下跌1-2%买入10%，直至满仓150%-170%。
     （2）卖出，上证000001.SH（2010-2022）5次买入，100%胜率，买点-13%基本接近最低点（-14%仅3个买点100%胜率，12%3胜1负，，11%5胜1负，10%胜2负，所有负点在-13%设置下均为胜点，提前买入的效果非常差，而且并没有明显增加交易机会。 （-13%，+3%）为000001.SZ最优参数

    2.Turtle 右侧交易，追涨不追跌
      (1) 唐期安通道cross(20,10) N=ATR(20) 等仓位(最大5仓)，图表分析，基本所有上升趋势都抓住了交易机会
      (2) 仓位<=5 
      (3) 买入 close[0]> self.high_line[0]
      (4) 止损 self.buyprice < close- 2N 
      (5) 止盈 close[0] < self.low_line[0]
    
    3. 399001.SZ，2010-20221022， Ma_Diff_PCt(-15,+3)终值268 7胜0负 ，Ma_Diff_PCt(-13,+3)终值191 7胜1负，Ma_Diff_PCt（-10，+3）7胜2负。失败的都是在高参数是成功的==信号买早了，分别增加了1，2次成功交易
       图表(-15，+3)7次==100%均接近价格最低位，(-13,+3)5次==62.5%接近最低位90%，(-10,+3), (-10,+3)3次==27%接近最低位置90%
       策略 (-10,+3) -10 =30%，每增加-1增加15%的仓位，-11==10% -12==15% -13==20% -14=20% -15=融资70% 满仓150%-170%
       策略 (-10,+3) -10 =30%，每增加-1增加15%的仓位，-11==10% -12==15% -13==20% -14=20% -15=融资70% 满仓150%-170%


    4. list of trade-code 2022.10.26
      恒生科技ETF      513130.SH    规模129亿份    恒生科技指数 HSTECH.hk       T+0
      恒生科技30ETF    513010.SH    规模25亿份                                 T+0
      恒生ETF          159920.SZ    规模147亿份    恒生指数       HIG.HK       T+0
      黄金ETF          518880.SH    规模98亿份                                 T+0
      上证50ETF        510050.SH    规模670亿份    上证50指数     000016.SH
      创业50ETF        159949.SZ    规模92亿份     创业板50指数   399673.SZ
      创业板ETF        159915.SZ    规模160亿份    创业板指数     399006.SZ
      上证ETF                                     上证指数       000001.SH
      科创50ETF        588000.SH    规模298亿份    科创50指数     000688.SH    生物/半导体为主 成立只有2年
      中证1000ETF      512100.SH    规模103亿份    中证1000指数   000852.SH    成立日期20160929
      中证1000指数ETF  159633.SH    规模57亿份     中证1000指数   000852.SH    成立日期20220722
      沪深300ETF       510300.SH    规模512亿份    沪深300指数

