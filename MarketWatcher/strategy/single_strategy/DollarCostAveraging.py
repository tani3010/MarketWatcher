# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class DollarCostAveraging(BaseStrategy):
    def __init__(self, broker, data, params):
        self.buy_amount = 10000
        self.buy_period = 100
        self.count = 0
        self.cash_total = 0

        super().__init__(broker, data, params)
        self.strategy_name = 'DollarCostAveraging'
        # self.buy_datetime = self.data.df.resample('Q').ax
        self.buy_datetime = self.data.df.groupby([self.data.df.index.year, self.data.df.index.month]).tail(1).index # monthly

    def init(self):
        self.cash_total = self.equity
    
    def next(self):
        self.count += 1
        # if not (self.count % self.buy_period):
        if self.data.index[-1] in self.buy_datetime:
            cash_left = self.cash_total - sum(x.entry_price*x.size for x in self.trades)
            if (self.buy_amount >= self.data.Close[-1]):
                self.buy(size=self.buy_amount // self.data.Close[-1])
