# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class BuyTheDips(BaseStrategy):
    def __init__(self, broker, data, params):
        self.BuyTheDips_level = -0.1
        self.set_optimization_parameter(
            BuyTheDips_level=[-x*0.01 for x in range(5, 10, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'BuyTheDips'

    def init(self):
        super().init()
        self.pct_change = self.metrics.pct_change(self.data, self.df_freq)

    def next(self):
        super().next()
        if self.pct_change[-1] <= self.BuyTheDips_level:
            self.buy()
