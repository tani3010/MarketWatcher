# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from database.FundingRateTableManager import fetch_funding_rate
from logging import getLogger
import numpy as np
logger = getLogger(__name__)

class FundingRateHedge(BaseStrategy):
    def __init__(self, broker, data, params):
        self.FundingRateHedge_level = -0.035 * 0.01
        self.set_optimization_parameter(
            FundingRateHedge_level=[-x*0.01*0.01 for x in range(0, 10, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'FundingRateHedge'
        self.pre_load()

    def pre_load(self):
        self.df_funding_rate = fetch_funding_rate('phemex', 'ETHUSD ETH-Margin')
        self.df_funding_rate = self.data.df.merge(self.df_funding_rate, how='left', left_index=True, right_index=True)

    def init(self):
        super().init()
        self.funding_rate = self.metrics.dummy(self.df_funding_rate, '1H', 'funding_rate', name='funding rate')
        self.hedge_timing = self.metrics.dummy(self.df_funding_rate, '1H', 'funding_rate', name='hedge timing', scatter=True)

        self.hedge_timing.df.iloc[0] = 0
        for i in reversed(range(1, len(self.funding_rate.df))):
            if not np.isnan(self.df_funding_rate['funding_rate'].iloc[i]) and np.isnan(self.df_funding_rate['funding_rate'].iloc[i-1]):
                self.hedge_timing.df.iloc[i] = 1
            else:
                self.hedge_timing.df.iloc[i] = 0

    def next(self):
        super().next()
#        if self.trades:
#            self.position.close()

        for trade in self.trades:
            if trade.tp is None:
                trade.tp = trade.entry_price

        if self.hedge_timing[-1] == 1 and self.funding_rate[-1] <= self.FundingRateHedge_level:
            self.buy()
