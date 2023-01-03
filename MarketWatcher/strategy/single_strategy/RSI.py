# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class RSI(BaseStrategy):
    def __init__(self, broker, data, params):
        self.RSI_timeperiod = 14
        self.RSI_upper_threshold = 70
        self.RSI_lower_threshold = 30
        self.set_optimization_parameter(
            RSI_timeperiod=range(10, 50, 5),
            RSI_upper_threshold=range(70, 80, 2),
            RSI_lower_threshold=range(20, 30, 2)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'RSI'

    def init(self):
        super().init()
        self.rsi = self.metrics.RSI(self.data, self.df_freq, self.RSI_timeperiod)

    def next(self):
        super().next()
        if self.rsi[-1] >= self.RSI_upper_threshold:
            self.position.close()
            self.sell()
        elif self.rsi[-1] <= self.RSI_lower_threshold:
            self.position.close()
            self.buy()

class ModifiedRSI(RSI):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.strategy_name = 'ModifiedRSI'
        self.RSI_timeperiod_rsi_ema = 5

    def init(self):
        super().init()

    def next(self):
        rsi_avg = self.rsi[-15:-1].mean()
        if self.rsi[-1] >= self.RSI_upper_threshold and self.rsi[-1] < rsi_avg:
            self.position.close()
            self.sell()
        elif self.rsi[-1] <= self.RSI_lower_threshold and self.rsi[-1] > rsi_avg:
            self.position.close()
            self.buy()

class ConnorsRSI(BaseStrategy):
    def __init__(self, broker, data, params):
        self.ConnorsRSI_timeperiod = 3
        self.ConnorsRSI_count = 2
        self.ConnorsRSI_percentage_rank = 100
        self.ConnorsRSI_upper_threshold = 90
        self.ConnorsRSI_lower_threshold = 10
        self.set_optimization_parameter(
            ConnorsRSI_timeperiod=range(3, 10, 1),
            ConnorsRSI_count=range(2, 10, 1),
            ConnorsRSI_percentage_rank=range(90, 110, 5),
            ConnorsRSI_upper_threshold=range(80, 95, 5),
            ConnorsRSI_lower_threshold=range(5, 20, 5)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'ConnorsRSI'

    def init(self):
        super().init()
        self.rsi = self.metrics.CONNORSRSI(
            self.data, self.df_freq, self.ConnorsRSI_timeperiod, self.ConnorsRSI_count, self.ConnorsRSI_percentage_rank)

    def next(self):
        super().next()
        if self.rsi[-1] >= self.ConnorsRSI_upper_threshold:
            self.position.close()
            self.sell()
        elif self.rsi[-1] <= self.ConnorsRSI_lower_threshold:
            self.position.close()
            self.buy()
