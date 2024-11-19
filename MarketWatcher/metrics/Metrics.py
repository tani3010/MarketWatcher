# -*- coding: utf-8 -*-

import talib
import numpy as np
import pandas as pd
from backtesting.lib import OHLCV_AGG, resample_apply

class Metrics(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def resample(df_ohlcv, rule, closed='right', label='right'):
        return df_ohlcv.resample(rule, closed=closed, label=label).agg(OHLCV_AGG).dropna()

    @staticmethod
    def _pct_change(df, rule, shift=1):
        return df.pct_change(shift)

    def pct_change(self, df_ohlcv, rule, shift=1):
        return resample_apply(rule, self._pct_change, df_ohlcv['Close'], shift, name='pct_change({})')

    @staticmethod
    def _RANGE_RSI(df, timeperiod):
        df['diff'] = df['Close'] - df['Open']
        df['HighRange'] = np.where(df['diff'] > 0, df['High'] - df['Open'], 0)
        df['LowRange'] = np.where(df['diff'] < 0, df['Low'] - df['Open'], 0)
        high_range_sum = df['HighRange'].rolling(timeperiod).sum()
        low_range_sum = df['LowRange'].rolling(timeperiod).sum()
        return high_range_sum / (high_range_sum - low_range_sum) * 100

    def RANGE_RSI(self, df_ohlcv, rule, timeperiod=14):
        return resample_apply(rule, self._RANGE_RSI, df_ohlcv.df[['Open', 'High', 'Low', 'Close']], timeperiod, name='RANGE_RSI({}, {})')

    @staticmethod
    def _CONNORSRSI(df, timeperiod, bar_count, percentage_rank):
        def STREAKS(series):
            geq = series >= series.shift(1)  # True if rising
            eq = series == series.shift(1)  # True if equal
            logic_table = pd.concat([geq, eq], axis=1)

            streaks = [0]  # holds the streak duration, starts with 0

            for row in logic_table.iloc[1:].itertuples():  # iterate through logic table
                if row[2]:  # same value as before
                    streaks.append(0)
                    continue
                last_value = streaks[-1]
                if row[1]:  # higher value than before
                    streaks.append(last_value + 1 if last_value >= 0 else 1)  # increase or reset to +1
                else:  # lower value than before
                    streaks.append(last_value - 1 if last_value < 0 else -1)  # decrease or reset to -1
            return np.array(streaks, dtype=float)

        def PERCENTRANK(series, n):
            x = np.array([sum(series[i+1-n:i+1] < series[i]) / n for i in range(len(series))])
            x[:n-1] = np.nan
            return x

        return (talib.RSI(df, timeperiod) + talib.RSI(STREAKS(df), bar_count) + PERCENTRANK(df, percentage_rank))/3

    def CONNORSRSI(self, df_ohlcv, rule, timeperiod=3, bar_count=2, percentage_rank=100):
        return resample_apply(rule, self._CONNORSRSI, df_ohlcv['Close'],
                              timeperiod, bar_count, percentage_rank,
                              name='CONNORSRSI({}, {}, {}, {})')

    @staticmethod
    def _dummy(df, *args, **kwargs):
        return df

    def dummy(self, df, rule, column, *args, **kwargs):
        return resample_apply(rule, self._dummy, df[column], *args, **kwargs)

    @staticmethod
    def BBANDS(df_ohlcv, rule, timeperiod=5, nbdevup=2, nbdevdn=2, matype=talib.MA_Type.SMA):
        return resample_apply(
            rule, talib.BBANDS, df_ohlcv['Close'],
            timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=talib.MA_Type.SMA)

    @staticmethod
    def RSI(df_ohlcv, rule, timeperiod=14):
        return resample_apply(
            rule, talib.RSI, df_ohlcv['Close'], timeperiod=timeperiod)

    @staticmethod
    def MA(df_ohlcv, rule, timeperiod=200, matype=talib.MA_Type.SMA):
        return resample_apply(
            rule, talib.MA, df_ohlcv['Close'], timeperiod=timeperiod, matype=talib.MA_Type.SMA)

    @staticmethod
    def SMA(df_ohlcv, rule, timeperiod=200, overlay=True):
        return resample_apply(
            rule, talib.SMA, df_ohlcv['Close'], timeperiod=timeperiod, overlay=overlay)

    @staticmethod
    def EMA(df_ohlcv, rule, timeperiod=200):
        return resample_apply(
            rule, talib.EMA, df_ohlcv['Close'], timeperiod=timeperiod)

    @staticmethod
    def WMA(df_ohlcv, rule, timeperiod=200):
        return resample_apply(
            rule, talib.WMA, df_ohlcv['Close'], timeperiod=timeperiod)

    @staticmethod
    def _SAR(df, acceleration=0, maximum=0):
        return talib.SAR(df['High'], df['Low'], acceleration=acceleration, maximum=maximum)

    def SAR(self, df_ohlcv, rule, acceleration=0, maximum=0):
        return resample_apply(
            rule, self._SAR, df_ohlcv.df[['High', 'Low']], acceleration, maximum, name='SAR({}, {}, {})')

    @staticmethod
    def HT_TRENDLINE(df_ohlcv, rule):
        return resample_apply(
            rule, talib.HT_TRENDLINE, df_ohlcv['Close'])

    @staticmethod
    def MACD_org(df_ohlcv, rule, fastperiod=12, slowperiod=26, signalperiod=9):
        return resample_apply(
            rule, talib.MACD, df_ohlcv['Close'], fastperiod, slowperiod, signalperiod)

    def MACD(self, df_ohlcv, rule, fastperiod=12, slowperiod=26, signalperiod=9):
        return resample_apply(
            rule, self._MACD, df_ohlcv.df['Close'], fastperiod, slowperiod, signalperiod,
            histogram=[False, False, True, True, True, True],
            color=['#2962FF', '#FF6D00', '#26A69A', '#B2DFDB', '#FF5252', '#FFCDD2'],
            name='MACD({}, {}, {}, {})')

    @staticmethod
    def _MACD_old(df, fastperiod=12, slowperiod=26, signalperiod=9):
        macd, macd_signal, macd_hist = talib.MACD(df, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=slowperiod)
        return [macd, macd_signal, macd_hist]

    @staticmethod
    def _MACD(df, fastperiod=12, slowperiod=26, signalperiod=9):
        macd, macd_signal, macd_hist = talib.MACD(df, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=slowperiod)

        macd_hist_diff = macd_hist.diff()

        macd_hist_positive_deep = macd_hist.copy()
        macd_hist_positive_light = macd_hist.copy()
        macd_hist_negative_deep = macd_hist.copy()
        macd_hist_negative_light = macd_hist.copy()

        macd_hist_positive_deep = np.where((macd_hist > 0) & (macd_hist_diff > 0), macd_hist.values, np.nan)
        macd_hist_positive_light = np.where((macd_hist > 0) & (macd_hist_diff < 0), macd_hist.values, np.nan)
        macd_hist_negative_deep = np.where((macd_hist < 0) & (macd_hist_diff < 0), macd_hist.values, np.nan)
        macd_hist_negative_light = np.where((macd_hist < 0) & (macd_hist_diff > 0), macd_hist.values, np.nan)

        return [macd, macd_signal, macd_hist_positive_deep, macd_hist_positive_light, macd_hist_negative_deep, macd_hist_negative_light]

    @staticmethod
    def _ULTOSC(df, timeperiod1=7, timeperiod2=14, timeperiod3=28):
        return talib.ULTOSC(
            df['High'], df['Low'], df['Close'],
            timeperiod1=timeperiod1, timeperiod2=timeperiod2, timeperiod3=timeperiod3)

    def ULTOSC(self, df_ohlcv, rule, timeperiod1=7, timeperiod2=14, timeperiod3=28):
        return resample_apply(
            rule, self._ULTOSC, df_ohlcv.df[['High', 'Low', 'Close']],
            timeperiod1, timeperiod2, timeperiod3, name='ULTOSC({}, {}, {}, {})')

    @staticmethod
    def _CDLHIKKAKEMOD(df):
        return talib.CDLHIKKAKEMOD(df['Open'], df['High'], df['Low'], df['Close'])

    def CDLHIKKAKEMOD(self, df_ohlcv, rule):
        return resample_apply(
            rule, self._CDLHIKKAKEMOD, df_ohlcv.df[['Open', 'High', 'Low', 'Close']])

    @staticmethod
    def _ATR(df, timeperiod):
        return talib.ATR(df['High'], df['Low'], df['Close'], timeperiod)

    def ATR(self, df_ohlcv, rule, timeperiod):
        return resample_apply(
            rule, self._ATR, df_ohlcv.df[['High', 'Low', 'Close']], timeperiod, name='ATR({}, {})')

    @staticmethod
    def _STOCH(df, fastk_period=5, slowk_period=3, slowd_period=3):
        return talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=fastk_period, slowk_period=slowk_period, slowd_period=slowd_period)

    def STOCH(self, df_ohlcv, rule, fastk_period=5, slowk_period=3 ,slowd_period=3):
        return resample_apply(
            rule, self._STOCH, df_ohlcv.df[['High', 'Low', 'Close']],
            fastk_period, slowk_period, slowd_period, name='STOCH({}, {}, {}, {})')

    @staticmethod
    def _NATR(df, timeperiod):
        return talib.NATR(df['High'], df['Low'], df['Close'], timeperiod)

    def NATR(self, df_ohlcv, rule, timeperiod):
        return resample_apply(rule, self._NATR, df_ohlcv.df[['High', 'Low', 'Close']], timeperiod, name='NATR({}, {})')

    @staticmethod
    def _TRANGE(df):
        return talib.TRANGE(df['High'], df['Low'], df['Close'])

    def TRANGE(self, df_ohlcv, rule):
        return resample_apply(rule, self._TRANGE, df_ohlcv.df[['High', 'Low', 'Close']], name='TRANGE({})')

    @staticmethod
    def _WilliamsFractal(df, timeperiod=2, isBull=True, center=False):
        window = 2 * timeperiod + 1
        bears = df['High'].rolling(window, center=center).apply(lambda x: x[timeperiod] == max(x), raw=True)
        bulls = df['Low'].rolling(window, center=center).apply(lambda x: x[timeperiod] == min(x), raw=True)
        return bears if isBull else bulls # [bears, bulls]

    def WilliamsFractal(self, df_ohlcv, rule, timeperiod=2, isBull=True):
        name = 'WilliamsFractal_{}'.format('Bull' if isBull else 'Bear') + '({}, {}, {})'
        return resample_apply(
            rule, self._WilliamsFractal, df_ohlcv.df[['High', 'Low']], timeperiod, isBull, scatter=True, name=name)
