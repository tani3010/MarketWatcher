# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class EngulfingBar(BaseStrategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.strategy_name = 'EngulfingBar'

    def next(self):
        super().next()

        if self.data.Open[-1] < self.data.Close[-2] < self.data.Open[-2] < self.data.Close[-1]:
            self.buy(tp=self.data.High[-1])

        #elif self.data.Close[-1] < self.data.Open[-2] < self.data.Close[-2] < self.data.Open[-1]:
        #    eps = 0.0011
        #    self.sell(tp=self.data.Low[-1] * (1 - eps))
