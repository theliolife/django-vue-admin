# scripts/target_stk_factor_base.py

# 导入tushare
import os
import talib
import numpy as np
import pymysql
import pandas as pd
import MyTT
from sqlalchemy import create_engine

db = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USERNAME"),
    passwd=os.environ.get("DB_PASSWORD"),
    db=os.environ.get("DB_DATABASE"),
    port=int(os.environ.get("DB_PORT"))
)

engine = create_engine(os.environ.get("CREAT_ENGINE"))


def run():

    cursor = db.cursor()

    cursor.execute(r"select ts_code from tu_share_stock_basic where id > 297")
    stocks = cursor.fetchall()

    for stock in stocks:
        target = dict()
        stockade = stock[0]
        print(stockade)

        # 这里把周线月线一起做了
        cursor.execute(
            r"select ts_code,trade_date,close,open,high,low,vol from tu_share_price_daily where trade_date > '2021-01-01' AND ts_code = %s",
            stockade)
        prices = cursor.fetchall()

        prices_pd = pd.DataFrame(prices, columns=['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'vol'])
        prices_pd['close'] = pd.to_numeric(prices_pd['close'])
        prices_pd['open'] = pd.to_numeric(prices_pd['open'])
        prices_pd['high'] = pd.to_numeric(prices_pd['high'])
        prices_pd['low'] = pd.to_numeric(prices_pd['low'])
        prices_pd['vol'] = pd.to_numeric(prices_pd['vol'])

        CLOSE = prices_pd.close.values
        OPEN = prices_pd.open.values  # 基础数据定义，只要传入的是序列都可以
        HIGH = prices_pd.high.values
        LOW = prices_pd.low.values  # 例如 CLOSE=list(df.close) 都是一样
        VOL = prices_pd.vol.values

        if len(CLOSE) == 0:
            continue

        target['close'] = CLOSE
        target['open'] = OPEN
        target['high'] = HIGH
        target['low'] = LOW
        target['vol'] = VOL

        # Momentum Indicators 动量指标
        target['ts_code'] = prices_pd.ts_code.values
        target['trade_date'] = prices_pd.trade_date.values

        # MACD
        target['dif'], target['dem'], target['histogram'] = talib.MACD(CLOSE, fastperiod=12, slowperiod=26, signalperiod=9)

        # KDJ
        target['K'], target['D'], target['J'] = MyTT.KDJ(CLOSE, HIGH, LOW)

        # RSI
        target['rsi_6'] = MyTT.RSI(CLOSE, 6)
        target['rsi_12'] = MyTT.RSI(CLOSE, 12)
        target['rsi_24'] = MyTT.RSI(CLOSE, 24)
        # RSI及四六日斜率
        target['rsi_2_slope'] = MyTT.SLOPE(target['rsi_6'], 2)
        target['rsi_4_slope'] = MyTT.SLOPE(target['rsi_6'], 4)

        # Volume Indicators 成交量指标
        target['AD'] = talib.AD(HIGH, LOW, CLOSE, VOL)
        target['ADOSC'] = talib.ADOSC(HIGH, LOW, CLOSE, VOL)
        target['OBV'] = talib.OBV(CLOSE, VOL)

        # Volatility Indicators 波动性指标
        target['ATR'] = talib.ATR(HIGH, LOW, CLOSE)

        # Price Transform 价格指标
        target['ma5'] = MyTT.MA(CLOSE, 5)  # 获取5日均线序列
        target['ma10'] = MyTT.MA(CLOSE, 10)  # 获取10日均线序列
        # 布林线
        target['upperband'], target['middleband'], target['lowerband'] = talib.BBANDS(CLOSE, timeperiod=5, nbdevup=2,
                                                                                      nbdevdn=2, matype=0)
        # Cycle Indicators 周期指标
        target['HT_DCPERIOD'] = talib.HT_DCPERIOD(CLOSE)
        target['HT_TRENDMODE'] = talib.HT_TRENDMODE(CLOSE)

        # Pattern Recognition 形态识别
        # 多指标形态
        target['CDL3INSIDE'] = talib.CDL3INSIDE(OPEN, HIGH, LOW, CLOSE)
        target['CDL3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(OPEN, HIGH, LOW, CLOSE)
        target['CDL3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(OPEN, HIGH, LOW, CLOSE)
        target['CDLBELTHOLD'] = talib.CDLBELTHOLD(OPEN, HIGH, LOW, CLOSE)
        target['CDLBREAKAWAY'] = talib.CDLBREAKAWAY(OPEN, HIGH, LOW, CLOSE)
        target['CDLHARAMI'] = talib.CDLHARAMI(OPEN, HIGH, LOW, CLOSE)
        target['CDLXSIDEGAP3METHODS'] = talib.CDLXSIDEGAP3METHODS(OPEN, HIGH, LOW, CLOSE)

        # 空指标形态
        target['CDL2CROWS'] = talib.CDL2CROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(OPEN, HIGH, LOW, CLOSE)
        target['CDLDARKCLOUDCOVER'] = talib.CDLDARKCLOUDCOVER(OPEN, HIGH, LOW, CLOSE)
        target['CDLIDENTICAL3CROWS'] = talib.CDLIDENTICAL3CROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDLINNECK'] = talib.CDLINNECK(OPEN, HIGH, LOW, CLOSE)
        target['CDLSHOOTINGSTAR'] = talib.CDLSHOOTINGSTAR(OPEN, HIGH, LOW, CLOSE)

        # 持续指标形态
        target['CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(OPEN, HIGH, LOW, CLOSE)
        target['CDLHIKKAKE'] = talib.CDLHIKKAKE(OPEN, HIGH, LOW, CLOSE)
        target['CDLONNECK'] = talib.CDLONNECK(OPEN, HIGH, LOW, CLOSE)
        target['CDLSEPARATINGLINES'] = talib.CDLSEPARATINGLINES(OPEN, HIGH, LOW, CLOSE)
        target['CDLTHRUSTING'] = talib.CDLTHRUSTING(OPEN, HIGH, LOW, CLOSE)

        # 反转指标形态
        target['CDLABANDONEDBABY'] = talib.CDLABANDONEDBABY(OPEN, HIGH, LOW, CLOSE)
        target['CDLDOJISTAR'] = talib.CDLDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLDRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(OPEN, HIGH, LOW, CLOSE)
        target['CDLEVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLEVENINGSTAR'] = talib.CDLEVENINGSTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLHARAMICROSS'] = talib.CDLHARAMICROSS(OPEN, HIGH, LOW, CLOSE)
        target['CDLHIGHWAVE'] = talib.CDLHIGHWAVE(OPEN, HIGH, LOW, CLOSE)
        target['CDLHOMINGPIGEON'] = talib.CDLHOMINGPIGEON(OPEN, HIGH, LOW, CLOSE)
        target['CDLINVERTEDHAMMER'] = talib.CDLINVERTEDHAMMER(OPEN, HIGH, LOW, CLOSE)
        target['CDLLADDERBOTTOM'] = talib.CDLLADDERBOTTOM(OPEN, HIGH, LOW, CLOSE)
        target['CDLSTALLEDPATTERN'] = talib.CDLSTALLEDPATTERN(OPEN, HIGH, LOW, CLOSE)
        target['CDLTRISTAR'] = talib.CDLTRISTAR(OPEN, HIGH, LOW, CLOSE)
        # 底部反转
        target['CDLCONCEALBABYSWALL'] = talib.CDLCONCEALBABYSWALL(OPEN, HIGH, LOW, CLOSE)
        target['CDLGRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(OPEN, HIGH, LOW, CLOSE)
        target['CDLHAMMER'] = talib.CDLHAMMER(OPEN, HIGH, LOW, CLOSE)
        target['CDLMORNINGDOJISTAR'] = talib.CDLMORNINGDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLMORNINGSTAR'] = talib.CDLMORNINGSTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLPIERCING'] = talib.CDLPIERCING(OPEN, HIGH, LOW, CLOSE)

        # Statistic Functions 统计函数
        # Math Transform 数学变换
        # Math Operators 数学运算符

        # 指标曲率
        # MA5曲率
        target['ma5_slope'] = MyTT.SLOPE(target['ma5'], 5)
        # MA10曲率
        target['ma10_slope'] = MyTT.SLOPE(target['ma10'], 10)

        target = pd.DataFrame(target)
        target.fillna(0, inplace=True)

        # MACD曲率
        # target['macd_slope'] = talib.LINEARREG_SLOPE(target['histogram'], timeperiod=2)
        target['macd_slope'] = MyTT.SLOPE(target['histogram'], 2)

        # 统计
        # macd 持续天数 大于零小于零
        target['macd_BARSLAST_0'] = MyTT.BARSLAST(target['histogram'] > 0)
        target['macd_BARSLAST_1'] = MyTT.BARSLAST(target['histogram'] < 0)
        target['macd_slope_1'] = MyTT.BARSLAST(target['macd_slope'] > 0)
        target['macd_slope_2'] = MyTT.BARSLAST(target['macd_slope'] < 0)

        # price单日曲率
        target['price_slope'] = MyTT.SLOPE(CLOSE, 2)
        # vol单日曲率
        target['vol_slope'] = MyTT.SLOPE(VOL, 2)
        # MA5曲率
        target['ma5_slope'] = MyTT.SLOPE(target['ma5'], 5)
        # MA10曲率
        target['ma10_slope'] = MyTT.SLOPE(target['ma10'], 10)

        target = pd.DataFrame(target)

        # 交叉
        target['zero_line'] = np.linspace(0, 0, len(target['histogram']))

        # macd
        dif, dea, macd = MyTT.MACD(CLOSE)

        # 交叉
        zero_line = np.linspace(0, 0, len(macd))
        target['macd_cross_up'] = MyTT.CROSS(macd, zero_line)
        target['macd_cross_down'] = MyTT.CROSS(zero_line, macd)

        # 五日均线上穿十日均线
        target['ma5_cross_ma10'] = MyTT.CROSS(target['ma5'].values, target['ma10'].values)
        # 三天内金叉
        target['cross_3_day'] = MyTT.EXIST(CLOSE > OPEN, 5)

        # 威科夫形态

        # 未来十天收盘价涨跌
        close = prices_pd.close
        for day in range(1, 10):
            tmp_close_data = close.shift(periods=-day)
            target["close_day" + str(day)] = np.subtract(tmp_close_data, CLOSE)

        target["上一次大于0"] = MyTT.BARSLAST(target['histogram'] > 0)
        # df = get_stk_factor(trade_date=date)
        target.to_sql('target_stk_factor_base', engine, if_exists='append', index=False)

    runWeek()


def runWeek():
    cursor = db.cursor()

    cursor.execute(r"select ts_code from tu_share_stock_basic")
    stocks = cursor.fetchall()

    for stock in stocks:
        target = dict()
        stockade = stock[0]

        # 这里把周线月线一起做了
        cursor.execute(
            r"select ts_code,trade_date,close,open,high,low,vol from tu_share_price_weekly where trade_date > '2021-01-01' AND ts_code = %s",
            stockade)
        prices = cursor.fetchall()

        prices_pd = pd.DataFrame(prices, columns=['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'vol'])
        prices_pd['close'] = pd.to_numeric(prices_pd['close'])
        prices_pd['open'] = pd.to_numeric(prices_pd['open'])
        prices_pd['high'] = pd.to_numeric(prices_pd['high'])
        prices_pd['low'] = pd.to_numeric(prices_pd['low'])
        prices_pd['vol'] = pd.to_numeric(prices_pd['vol'])

        CLOSE = prices_pd.close.values
        OPEN = prices_pd.open.values  # 基础数据定义，只要传入的是序列都可以
        HIGH = prices_pd.high.values
        LOW = prices_pd.low.values  # 例如 CLOSE=list(df.close) 都是一样
        VOL = prices_pd.vol.values
        if len(CLOSE) == 0:
            continue

        target['close'] = CLOSE
        target['open'] = OPEN
        target['high'] = HIGH
        target['low'] = LOW
        target['vol'] = VOL

        # Momentum Indicators 动量指标
        target['ts_code'] = prices_pd.ts_code.values
        target['trade_date'] = prices_pd.trade_date.values

        # MACD
        target['dif'], target['dem'], target['histogram'] = talib.MACD(CLOSE, fastperiod=12, slowperiod=26, signalperiod=9)

        # KDJ
        target['K'], target['D'], target['J'] = MyTT.KDJ(CLOSE, HIGH, LOW)

        # RSI
        target['rsi_6'] = MyTT.RSI(CLOSE, 6)
        target['rsi_12'] = MyTT.RSI(CLOSE, 12)
        target['rsi_24'] = MyTT.RSI(CLOSE, 24)
        # RSI及四六日斜率
        target['rsi_2_slope'] = MyTT.SLOPE(target['rsi_6'], 2)
        target['rsi_4_slope'] = MyTT.SLOPE(target['rsi_6'], 4)

        # Volume Indicators 成交量指标
        target['AD'] = talib.AD(HIGH, LOW, CLOSE, VOL)
        target['ADOSC'] = talib.ADOSC(HIGH, LOW, CLOSE, VOL)
        target['OBV'] = talib.OBV(CLOSE, VOL)

        # Volatility Indicators 波动性指标
        target['ATR'] = talib.ATR(HIGH, LOW, CLOSE)

        # Price Transform 价格指标
        target['ma5'] = MyTT.MA(CLOSE, 5)  # 获取5日均线序列
        target['ma10'] = MyTT.MA(CLOSE, 10)  # 获取10日均线序列
        # 布林线
        target['upperband'], target['middleband'], target['lowerband'] = talib.BBANDS(CLOSE, timeperiod=5, nbdevup=2,
                                                                                      nbdevdn=2, matype=0)
        # Cycle Indicators 周期指标
        target['HT_DCPERIOD'] = talib.HT_DCPERIOD(CLOSE)
        target['HT_TRENDMODE'] = talib.HT_TRENDMODE(CLOSE)

        # Pattern Recognition 形态识别
        # 多指标形态
        target['CDL3INSIDE'] = talib.CDL3INSIDE(OPEN, HIGH, LOW, CLOSE)
        target['CDL3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(OPEN, HIGH, LOW, CLOSE)
        target['CDL3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(OPEN, HIGH, LOW, CLOSE)
        target['CDLBELTHOLD'] = talib.CDLBELTHOLD(OPEN, HIGH, LOW, CLOSE)
        target['CDLBREAKAWAY'] = talib.CDLBREAKAWAY(OPEN, HIGH, LOW, CLOSE)
        target['CDLHARAMI'] = talib.CDLHARAMI(OPEN, HIGH, LOW, CLOSE)
        target['CDLXSIDEGAP3METHODS'] = talib.CDLXSIDEGAP3METHODS(OPEN, HIGH, LOW, CLOSE)

        # 空指标形态
        target['CDL2CROWS'] = talib.CDL2CROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(OPEN, HIGH, LOW, CLOSE)
        target['CDLDARKCLOUDCOVER'] = talib.CDLDARKCLOUDCOVER(OPEN, HIGH, LOW, CLOSE)
        target['CDLIDENTICAL3CROWS'] = talib.CDLIDENTICAL3CROWS(OPEN, HIGH, LOW, CLOSE)
        target['CDLINNECK'] = talib.CDLINNECK(OPEN, HIGH, LOW, CLOSE)
        target['CDLSHOOTINGSTAR'] = talib.CDLSHOOTINGSTAR(OPEN, HIGH, LOW, CLOSE)

        # 持续指标形态
        target['CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(OPEN, HIGH, LOW, CLOSE)
        target['CDLHIKKAKE'] = talib.CDLHIKKAKE(OPEN, HIGH, LOW, CLOSE)
        target['CDLONNECK'] = talib.CDLONNECK(OPEN, HIGH, LOW, CLOSE)
        target['CDLSEPARATINGLINES'] = talib.CDLSEPARATINGLINES(OPEN, HIGH, LOW, CLOSE)
        target['CDLTHRUSTING'] = talib.CDLTHRUSTING(OPEN, HIGH, LOW, CLOSE)

        # 反转指标形态
        target['CDLABANDONEDBABY'] = talib.CDLABANDONEDBABY(OPEN, HIGH, LOW, CLOSE)
        target['CDLDOJISTAR'] = talib.CDLDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLDRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(OPEN, HIGH, LOW, CLOSE)
        target['CDLEVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLEVENINGSTAR'] = talib.CDLEVENINGSTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLHARAMICROSS'] = talib.CDLHARAMICROSS(OPEN, HIGH, LOW, CLOSE)
        target['CDLHIGHWAVE'] = talib.CDLHIGHWAVE(OPEN, HIGH, LOW, CLOSE)
        target['CDLHOMINGPIGEON'] = talib.CDLHOMINGPIGEON(OPEN, HIGH, LOW, CLOSE)
        target['CDLINVERTEDHAMMER'] = talib.CDLINVERTEDHAMMER(OPEN, HIGH, LOW, CLOSE)
        target['CDLLADDERBOTTOM'] = talib.CDLLADDERBOTTOM(OPEN, HIGH, LOW, CLOSE)
        target['CDLSTALLEDPATTERN'] = talib.CDLSTALLEDPATTERN(OPEN, HIGH, LOW, CLOSE)
        target['CDLTRISTAR'] = talib.CDLTRISTAR(OPEN, HIGH, LOW, CLOSE)
        # 底部反转
        target['CDLCONCEALBABYSWALL'] = talib.CDLCONCEALBABYSWALL(OPEN, HIGH, LOW, CLOSE)
        target['CDLGRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(OPEN, HIGH, LOW, CLOSE)
        target['CDLHAMMER'] = talib.CDLHAMMER(OPEN, HIGH, LOW, CLOSE)
        target['CDLMORNINGDOJISTAR'] = talib.CDLMORNINGDOJISTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLMORNINGSTAR'] = talib.CDLMORNINGSTAR(OPEN, HIGH, LOW, CLOSE)
        target['CDLPIERCING'] = talib.CDLPIERCING(OPEN, HIGH, LOW, CLOSE)

        # Statistic Functions 统计函数
        # Math Transform 数学变换
        # Math Operators 数学运算符

        # 指标曲率
        # MA5曲率
        target['ma5_slope'] = MyTT.SLOPE(target['ma5'], 5)
        # MA10曲率
        target['ma10_slope'] = MyTT.SLOPE(target['ma10'], 10)

        target = pd.DataFrame(target)
        target.fillna(0, inplace=True)

        # MACD曲率
        # target['macd_slope'] = talib.LINEARREG_SLOPE(target['histogram'], timeperiod=2)
        target['macd_slope'] = MyTT.SLOPE(target['histogram'], 2)

        # 统计
        # macd 持续天数 大于零小于零
        target['macd_BARSLAST_0'] = MyTT.BARSLAST(target['histogram'] > 0)
        target['macd_BARSLAST_1'] = MyTT.BARSLAST(target['histogram'] < 0)
        target['macd_slope_1'] = MyTT.BARSLAST(target['macd_slope'] > 0)
        target['macd_slope_2'] = MyTT.BARSLAST(target['macd_slope'] < 0)

        # price单日曲率
        target['price_slope'] = MyTT.SLOPE(CLOSE, 2)
        # vol单日曲率
        target['vol_slope'] = MyTT.SLOPE(VOL, 2)
        # MA5曲率
        target['ma5_slope'] = MyTT.SLOPE(target['ma5'], 5)
        # MA10曲率
        target['ma10_slope'] = MyTT.SLOPE(target['ma10'], 10)

        target = pd.DataFrame(target)

        # 交叉
        target['zero_line'] = np.linspace(0, 0, len(target['histogram']))

        # macd
        dif, dea, macd = MyTT.MACD(CLOSE)

        # 交叉
        zero_line = np.linspace(0, 0, len(macd))
        target['macd_cross_up'] = MyTT.CROSS(macd, zero_line)
        target['macd_cross_down'] = MyTT.CROSS(zero_line, macd)

        # 五日均线上穿十日均线
        target['ma5_cross_ma10'] = MyTT.CROSS(target['ma5'].values, target['ma10'].values)
        # 三天内金叉
        target['cross_3_day'] = MyTT.EXIST(CLOSE > OPEN, 5)

        # 威科夫形态

        # 未来十天收盘价涨跌
        close = prices_pd.close
        for day in range(1, 10):
            tmp_close_data = close.shift(periods=-day)
            target["close_day" + str(day)] = np.subtract(tmp_close_data, CLOSE)

        target["上一次大于0"] = MyTT.BARSLAST(target['histogram'] > 0)
        # df = get_stk_factor(trade_date=date)
        target.to_sql('target_stk_factor_base_week', engine, if_exists='append', index=False)