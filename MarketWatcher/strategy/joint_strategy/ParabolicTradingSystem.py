# -*- coding: utf-8 -*-

from strategy.single_strategy.BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

# https://medium.com/@pethuelp/2nd-update-parabolic-theory-based-stock-trading-and-some-reflections-8579f348a2c7
# https://decodingmarkets.com/stock-trading-strategy-300/
# https://kernc.github.io/backtesting.py/doc/examples/Multiple%20Time%20Frames.html

class ParabolicTradingSystem(BaseStrategy):
    def __init__(self, broker, data, params):
        self.ParabolicTradingSystem_rsi_timeperiod_daily = 30  # Daily RSI lookback period
        self.ParabolicTradingSystem_rsi_timeperiod_weekly = 30  # Weekly
        self.ParabolicTradingSystem_level = 70
        self.set_optimization_parameter(
            ParabolicTradingSystem_rsi_timeperiod_daily=range(10, 35, 5),
            ParabolicTradingSystem_rsi_timeperiod_weekly=range(10, 35, 5),
            ParabolicTradingSystem_level=range(60, 100, 5)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'ParabolicTradingSystem'

    def init(self):
        super().init()
        self.ma10 = self.metrics.SMA(self.data, '1D', 10)
        self.ma20 = self.metrics.SMA(self.data, '1D', 20)
        self.ma50 = self.metrics.SMA(self.data, '1D', 50)
        self.ma100 = self.metrics.SMA(self.data, '1D', 100)        
        self.rsi_daily = self.metrics.RSI(
            self.data, '1D', self.ParabolicTradingSystem_rsi_timeperiod_daily)
        self.rsi_weekly = self.metrics.RSI(
            self.data, 'W-FRI', self.ParabolicTradingSystem_rsi_timeperiod_weekly)
        
    def next(self):
        price = self.data.Close[-1]
        if (not self.position and
            self.rsi_daily[-1] > self.ParabolicTradingSystem_level and
            self.rsi_weekly[-1] > self.ParabolicTradingSystem_level and
            self.rsi_weekly[-1] > self.rsi_daily[-1] and
            self.ma10[-1] > self.ma20[-1] > self.ma50[-1] > self.ma100[-1] and
            price > self.ma10[-1]):
            
            # Buy at market price on next open, but do
            # set 8% fixed stop loss.
            self.buy(sl=0.92 * price)
        
        # If the price closes 2% or more below 10-day MA
        # close the position, if any.
        elif price < 0.98 * self.ma10[-1]:
            self.position.close()