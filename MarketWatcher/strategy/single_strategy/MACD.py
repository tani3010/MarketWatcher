# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import crossover
from logging import getLogger
logger = getLogger(__name__)

class MACD(BaseStrategy):
    def __init__(self, broker, data, params):
        self.MACD_shifter = 1
        self.MACD_fast_period = 12
        self.MACD_slow_period = 26
        self.MACD_signal_period = 9
        self.set_optimization_parameter(
            MACD_shifter=range(1, 10),
            MACD_fast_period=range(9, 30, 3),
            MACD_slow_period=range(20, 60, 5),
            MACD_signal_period=range(5, 30, 5)
        )
        super().__init__(broker, data, params)      
        self.strategy_name = 'MACD'

    def init(self):
        super().init()
        self.macd = self.metrics.MACD(self.data, self.df_freq, self.MACD_fast_period, self.MACD_slow_period, self.MACD_signal_period)

    def next(self):
        super().next()
        if crossover(self.macd[0], self.macd[1]):
            self.position.close()
            self.buy()
        elif crossover(self.macd[1], self.macd[0]):
            self.position.close()
            self.sell()