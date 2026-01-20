# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class EngulfingBar(BaseStrategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.strategy_name = 'EngulfingBar'

    def next_org(self):
        super().next()

        if self.data.Open[-1] < self.data.Close[-2] < self.data.Open[-2] < self.data.Close[-1]:
            self.buy(tp=self.data.High[-1])

        #elif self.data.Close[-1] < self.data.Open[-2] < self.data.Close[-2] < self.data.Open[-1]:
        #    eps = 0.0011
        #    self.sell(tp=self.data.Low[-1] * (1 - eps))

    def next(self):
        super().next()

        if self.data.Open[-1] < self.data.Close[-2] < self.data.Open[-2] < self.data.Close[-1]:
            limit = 0.5 * (self.data.Close[-1] + self.data.Open[-1])
            tag = f'buy:{self.data._Data__i}'
            self.buy(tp=self.data.High[-1], limit=limit, tag=tag)

        elif self.data.Close[-1] < self.data.Open[-2] < self.data.Close[-2] < self.data.Open[-1]:
            eps = 0.0011
            limit = 0.5 * (self.data.Open[-1] + self.data.Close[-1])
            tag = f'sell:{self.data._Data__i}'
            self.sell(tp=self.data.Low[-1] * (1 - eps), limit=limit * (1 - eps), tag=tag)

        for _order in self.orders:
             nb_bar = self.data._Data__i - int(_order.tag.split(':')[-1])
             if nb_bar > 4:
                 _order.cancel()