# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import crossover
from logging import getLogger
logger = getLogger(__name__)

class StopLoss(BaseStrategy):
    def __init__(self, broker, data, params):
        self.StopLoss_loss_cut_level_pct = -0.05
        self.set_optimization_parameter(
            StopLoss_loss_cut_level_pct=[-x*0.01 for x in range(5, 10, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'StopLoss'
        self.loss_cut_level_pct = 0.05

    def next(self):
        super().next()
        for trade in self.trades:
            if self.trade.pl_pct < self.StopLoss_loss_cut_level_pct:
                self.trade.close()