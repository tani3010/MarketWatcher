# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class PerfectOrder(BaseStrategy):
    def __init__(self, broker, data, params):
        self.PerfectOrder_shifter = 1
        self.PerfectOrder_timeperiod_short = 5
        self.PerfectOrder_timeperiod_middle = 50
        self.PerfectOrder_timeperiod_long = 200
        self.set_optimization_parameter(
            PerfectOrder_timeperiod_short=range(5, 10),
            PerfectOrder_timeperiod_middle=range(30, 60),
            PerfectOrder_timeperiod_long=range(100, 300, 20)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'PerfectOrder'

    def init(self):
        super().init()
        self.ma_short = self.metrics.SMA(self.data, self.df_freq, self.PerfectOrder_timeperiod_short)
        self.ma_middle = self.metrics.SMA(self.data, self.df_freq, self.PerfectOrder_timeperiod_middle)
        self.ma_long = self.metrics.SMA(self.data, self.df_freq, self.PerfectOrder_timeperiod_long)
        self.rsi = self.metrics.RSI(self.data, self.df_freq, 14)

    def next(self):
        super().next()
        if self.ma_short[-self.PerfectOrder_shifter] > self.ma_middle[-self.PerfectOrder_shifter] > self.ma_long[-self.PerfectOrder_shifter]:
            for trade in self.trades:
                if trade.is_short:
                    trade.close()
            if len(self.trades) == 0:
                self.buy()
        elif self.ma_short[-self.PerfectOrder_shifter] < self.ma_middle[-self.PerfectOrder_shifter] < self.ma_long[-self.PerfectOrder_shifter]:
            for trade in self.trades:
                if trade.is_long:
                    trade.close()
            if len(self.trades) == 0:
                self.sell()
        else:
            self.position.close()
