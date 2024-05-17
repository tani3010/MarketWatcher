# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import crossover
from logging import getLogger
logger = getLogger(__name__)

class Stochastics(BaseStrategy):
    def __init__(self, broker, data, params):
        self.Stochastics_shifter = 1
        self.Stochastics_fastk_period = 5
        self.Stochastics_slowk_period = 3
        self.Stochastics_slowd_period = 3
        self.set_optimization_parameter(
            Stochastics_shifter=range(1, 10),
            Stochastics_fastk_period=range(5, 10, 1),
            Stochastics_slowk_period=range(3, 10, 1),
            Stochastics_slowd_period=range(1, 10, 1)
        )
        super().__init__(broker, data, params)      
        self.strategy_name = 'Stochastics'

    def init(self):
        super().init()
        self.stochastics = self.metrics.STOCH(self.data, self.df_freq, self.Stochastics_fastk_period, self.Stochastics_slowk_period, self.Stochastics_slowd_period)

    def next(self):
        super().next()
        if self.data._Data__i < self.PerfectOrderEMA_shifter:
            return

        if crossover(self.stochastics[0][-1], self.stochastics[1][-1]):
            self.position.close()
            self.buy()
        elif crossover(self.stochastics[1][-1], self.stochastics[0][-1]):
            self.position.close()
            self.sell()