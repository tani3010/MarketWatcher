# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class StopLoss(BaseStrategy):
    def __init__(self, broker, data, params):
        self.StopLoss_minimum_holding_timeperiod = 30
        self.StopLoss_loss_cut_level_pct = -0.05
        self.set_optimization_parameter(
            StopLoss_minimum_holding_timeperiod=range(0, 100, 5),
            StopLoss_loss_cut_level_pct=[-x*0.01 for x in range(5, 10, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'StopLoss'
        self.loss_cut_level_pct = 0.05

    def next(self):
        super().next()
        for trade in self.trades:
            duration = self.data._Data__i - trade.entry_bar
            if duration > self.StopLoss_minimum_holding_timeperiod:
                if trade.pl_pct <= self.StopLoss_loss_cut_level_pct:
                    trade.__tag = 'StopLoss'
                    trade.close()
