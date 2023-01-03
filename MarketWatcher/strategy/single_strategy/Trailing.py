# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from backtesting.lib import TrailingStrategy
import numpy as np

from logging import getLogger
logger = getLogger(__name__)

class Trailing(BaseStrategy, TrailingStrategy):
    def __init__(self, broker, data, params):
        self.n_atr = 2
        self.set_optimization_parameter(
            n_atr=range(2, 10, 1)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'Trailing'

    def init(self):
        super().init()
        # self.set_trailing_sl(self.n_atr)

    def next(self):
        super().next()
        
class PercentageTrailing(BaseStrategy):
    """
    A strategy with automatic trailing stop-loss, trailing the current
    price at distance of some percentage. Call
    `PercentageTrailingStrategy.set_trailing_sl()` to set said percentage
    (`5` by default). See [tutorials] for usage examples.
    [tutorials]: index.html#tutorials
    Remember to call `super().init()` and `super().next()` in your
    overridden methods.
    """
    def __init__(self, broker, data, params):
        self.PercentageTrailing_sl_pct = 0.05
        self.set_optimization_parameter(
            PercentageTrailing_sl_pct=[x*0.01 for x in range(1, 11)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'PercentageTrailing'

    def init(self):
        super().init()

    def set_trailing_sl(self, percentage: float=5):
        assert percentage > 0, "percentage must be greater than 0"
        """
        Sets the future trailing stop-loss as some (`percentage`)
        percentage away from the current price.
        """
        self.PercentageTrailing_sl_pct = percentage*0.01

    def next(self):
        super().next()
        index = len(self.data)-1
        for trade in self.trades:
            if trade.is_long:
                trade.sl = max(trade.sl or -np.inf, self.data.Close[index]*(1-self.PercentageTrailing_sl_pct))
            else:
                trade.sl = min(trade.sl or np.inf, self.data.Close[index]*(1+self.PercentageTrailing_sl_pct))