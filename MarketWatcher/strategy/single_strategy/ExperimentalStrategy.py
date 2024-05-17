# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class Experimental(BaseStrategy):
    def __init__(self, broker, data, params):
        self.RSI_shifter = 1
        self.RSI_timeperiod = 14
        self.RSI_lower_threshold = 30
        self.RSI_upper_threshold = 70
        self.set_optimization_parameter(
            RSI_shifter=range(1, 10),
            RSI_timeperiod=range(10, 50, 5),
            RSI_lower_threshold=range(20, 30, 2),
            RSI_upper_threshold=range(70, 80, 2)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'Experimental'

    def init(self):
        super().init()
        self.rsi = self.metrics.RSI(self.data, '15min', self.RSI_timeperiod)

    def next(self):
        super().next()
        if self.data._Data__i < self.RSI_shifter:
            return

        if self.rsi[-self.RSI_shifter] >= self.RSI_upper_threshold:
            if trade in self.trades():
                if trade.is_
            self.sell()
        elif self.rsi[-self.RSI_shifter] <= self.RSI_lower_threshold:
            self.buy()