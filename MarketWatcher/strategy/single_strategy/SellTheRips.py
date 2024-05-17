# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class SellTheRips(BaseStrategy):
    def __init__(self, broker, data, params):
        self.SellTheRips_shifter = 1
        self.SellTheRips_level = 0.1
        self.SellTheRips_take_profit_level = 0.05
        self.set_optimization_parameter(
            SellTheRips_shifter=range(1, 30, 2),
            SellTheRips_level=[x*0.01 for x in range(5, 10, 1)],
            SellTheRips_take_profit_level=[x*0.01 for x in range(5, 10, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'SellTheRips'

    def init(self):
        super().init()
        self.pct_change = self.metrics.pct_change(self.data, self.df_freq)

    def next(self):
        super().next()
        if self.data._Data__i < self.SellTheRips_shifter:
            return

        if self.pct_change[-self.SellTheRips_shifter] >= self.SellTheRips_level:
            self.sell(tp=self.data.Close[-1]*(1-self.SellTheRips_take_profit_level))
