# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import crossover
from logging import getLogger
logger = getLogger(__name__)

class GoldenCross(BaseStrategy):
    def __init__(self, broker, data, params):
        self.GoldenCross_timeperiod_short = 5
        self.GoldenCross_timeperiod_long = 25
        self.set_optimization_parameter(
            GoldenCross_timeperiod_short=range(5, 25, 5),
            GoldenCross_timeperiod_long=range(25, 50, 5)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'GoldenCross'

    def init(self):
        super().init()
        self.ma_short = self.metrics.SMA(self.data, self.df_freq, self.GoldenCross_timeperiod_short)
        self.ma_long = self.metrics.SMA(self.data, self.df_freq, self.GoldenCross_timeperiod_long)

    def next(self):
        super().next()
        if crossover(self.ma_short, self.ma_long):
            self.position.close()
            self.buy()
