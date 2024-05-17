# -*- coding: utf-8 -*-

from .JointStrategy import JointStrategy
from strategy.single_strategy.PerfectOrder import PerfectOrderEMA
from strategy.single_strategy.Stochastics import Stochastics

from logging import getLogger
logger = getLogger(__name__)

class ATRScalping(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[PerfectOrderEMA, Stochastics]):
        params = {
            'PerfectOrderEMA_timeperiod_long': 40,
            'PerfectOrderEMA_timeperiod_middle': 14,
            'PerfectOrderEMA_timeperiod_short': 5
        }

        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ATRScalping'
        self.atr_timeperiod = 14
        self.atr = self.metrics.ATR(self.data, self.df_freq, self.atr_timeperiod)
        self.PerfectOrderEMA_timeperiod_long = 40
        self.PerfectOrderEMA_timeperiod_middle = 14
        self.PerfectOrderEMA_timeperiod_short = 5

    def next(self):
        super().next()
        for trade in self.trades:
            if trade.is_short:
                if self.data.Close[-1] <= trade.entry_price - 3.0 * self.atr[-1]:
                    trade.close()
                elif self.data.Close[-1] >= trade.entry_price + 2.0 * self.atr[-1]:
                    trade.close()
            else:
                if self.data.Close[-1] >= trade.entry_price + 3.0 * self.atr[-1]:
                    trade.close()
                elif self.data.Close[-1] <= trade.entry_price - 2.0 * self.atr[-1]:
                    trade.close()

