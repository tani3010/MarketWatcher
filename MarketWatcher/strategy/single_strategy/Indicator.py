# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from database.FundingRateTableManager import fetch_funding_rate
from logging import getLogger
logger = getLogger(__name__)

class Indicator(BaseStrategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.strategy_name = 'Indicator'
        self.timeperiod_short = 5
        self.timeperiod_long = 25
        self.timeperiod_rsi = 14
        self.timeperiod_atr = 14
        self.pre_load()

    def pre_load(self):
        self.df_funding_rate = fetch_funding_rate('phemex', 'ETHUSD ETH-Margin')
        self.df_funding_rate = self.data.df.merge(self.df_funding_rate, how='left', left_index=True, right_index=True)

    def init(self):
        super().init()
        self.funding_rate = self.metrics.dummy(self.df_funding_rate, '1H', 'funding_rate')
        self.pct_change = self.metrics.pct_change(self.data, '1D')
        self.ma_short = self.metrics.SMA(self.data, '1D', self.timeperiod_short)
        self.ma_long = self.metrics.SMA(self.data, '1D', self.timeperiod_long)
        self.rsi = self.metrics.RSI(self.data, '1D', self.timeperiod_rsi)
        self.atr = self.metrics.ATR(self.data, '1D', self.timeperiod_atr)
        self.natr = self.metrics.NATR(self.data, '1D', self.timeperiod_atr)
        self.tr = self.metrics.TRANGE(self.data, '1D')
        self.sar = self.metrics.SAR(self.data, '1D', 10, 20)
        self.ht_trendline = self.metrics.HT_TRENDLINE(self.data, '1D')
        self.macd = self.metrics.MACD(self.data, '1D')
        self.ULTOSC = self.metrics.ULTOSC(self.data, '1D')
        self.CDLHIKKAKEMOD = self.metrics.CDLHIKKAKEMOD(self.data, '1D')
        self.williams_fractal_bulls = self.metrics.WilliamsFractal(self.data, '1D', 2, True)
        self.williams_fractal_bears = self.metrics.WilliamsFractal(self.data, '1D', 2, False)
        self.bband = self.metrics.BBANDS(self.data, '1D')

    def next(self):
        super().next()
