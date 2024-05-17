# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import SignalStrategy
from logging import getLogger
logger = getLogger(__name__)

class WilliamsFractal(BaseStrategy, SignalStrategy):
    def __init__(self, broker, data, params):
        self.WilliamsFractal_timeperiod =  2
        self.set_optimization_parameter(
            WilliamsFractal_timeperiod=range(2, 20, 1)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'WilliamsFractal'

    def init(self):
        super().init()
        self.bulls = self.metrics.WilliamsFractal(self.data, self.df_freq, self.WilliamsFractal_timeperiod, True)
        self.bears = self.metrics.WilliamsFractal(self.data, self.df_freq, self.WilliamsFractal_timeperiod, False)
        self.set_signal(self.bears, self.bulls)

    def next(self):
        super().next()
