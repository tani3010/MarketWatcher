# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
import numpy as np
logger = getLogger(__name__)

class RSI(BaseStrategy):
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
        self.strategy_name = 'RSI'

    def init(self):
        super().init()
        self.rsi = self.metrics.RSI(self.data, self.df_freq, self.RSI_timeperiod)

    def next(self):
        super().next()
        if self.data._Data__i < self.RSI_shifter:
            return

        if self.rsi[-self.RSI_shifter] >= self.RSI_upper_threshold:
            self.position.close()
            self.sell()
        elif self.rsi[-self.RSI_shifter] <= self.RSI_lower_threshold:
            self.position.close()
            self.buy()

class RSIRange(RSI):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.RSI_upper_threshold = 75
        self.strategy_name = 'RSIRange'

    def init(self):
        self.rsi = self.metrics.RANGE_RSI(self.data, self.df_freq, self.RSI_timeperiod)

class RSIDouble(RSI):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.RSI_upper_threshold = 75
        self.strategy_name = 'RSIDouble'

    def init(self):
        self.rsi_1day = self.metrics.RSI(self.data, '1D', self.RSI_timeperiod)
        self.rsi_4hour = self.metrics.RSI(self.data, '4H', self.RSI_timeperiod)

    def next(self):
        if self.data._Data__i < self.RSI_shifter:
            return

        # if self.rsi_1day[-self.RSI_shifter] >= self.RSI_upper_threshold and self.rsi_4hour[-self.RSI_shifter] >= self.RSI_upper_threshold:
        if self.rsi_4hour[-self.RSI_shifter] >= self.RSI_upper_threshold:
            for trade in self.trades:
                if trade.is_long:
                    trade.close()
            #if len(self.trades) == 0:
            #    self.sell()

        elif self.rsi_1day[-self.RSI_shifter] <= self.RSI_lower_threshold and self.rsi_4hour[-self.RSI_shifter] <= self.RSI_lower_threshold:
            for trade in self.trades:
                if trade.is_short:
                    trade.close()
            if len(self.trades) == 0:
                self.buy()

class RSIDouble4HTakeProfit(RSI):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.RSI_shifter = 5
        self.RSI_shifter_TP = 1
        self.strategy_name = 'RSIDouble'

    def init(self):
        self.rsi_1day = self.metrics.RSI(self.data, '1D', self.RSI_timeperiod)
        self.rsi_4hour = self.metrics.RSI(self.data, '4H', self.RSI_timeperiod)

    def next(self):
        if self.data._Data__i < self.RSI_shifter:
            return

        # if self.rsi_1day[-self.RSI_shifter] >= self.RSI_upper_threshold and self.rsi_4hour[-self.RSI_shifter] >= self.RSI_upper_threshold:
        if self.rsi_4hour[-self.RSI_shifter_TP] >= self.RSI_upper_threshold:
            for trade in self.trades:
                if trade.is_long:
                    trade.close()
            #if len(self.trades) == 0:
            #    self.sell()

        elif self.rsi_1day[-self.RSI_shifter] <= self.RSI_lower_threshold and self.rsi_4hour[-self.RSI_shifter] <= self.RSI_lower_threshold:
            for trade in self.trades:
                if trade.is_short:
                    trade.close()
            if len(self.trades) == 0:
                self.buy()


class RSIRangeDouble(RSIDouble):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.RSI_upper_threshold = 75
        self.strategy_name = 'RSIRangeDouble'

    def init(self):
        self.rsi_1day = self.metrics.RANGE_RSI(self.data, '1D', self.RSI_timeperiod)
        self.rsi_4hour = self.metrics.RANGE_RSI(self.data, '4H', self.RSI_timeperiod)

class TrendFollowingRSIDouble(BaseStrategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.RSI_timeperiod = 14
        self.RSI_upper_threshold = 70
        self.RSI_lower_threshold = 30
        self.strategy_name = 'TrendFollowingRSIDouble'

    def init(self):
        self.rsi_1D = self.metrics.RSI(self.data, '1D', self.RSI_timeperiod)
        self.rsi_4H = self.metrics.RSI(self.data, '4H', self.RSI_timeperiod)
        self.rsi_1W = self.metrics.RSI(self.data, '1W', self.RSI_timeperiod)
        
        # for perfect order
        self.sma_14W = self.metrics.SMA(self.data, '1W', 14)
        self.sma_21W = self.metrics.SMA(self.data, '1W', 21)
        self.sma_35W = self.metrics.SMA(self.data, '1W', 35)
        
        self.is_rsi_up_trending = None

    @staticmethod
    def is_perfect_order(short, middle, long):
        if short >= middle >= long:
            return 1
        elif short <= middle <= long:
            return -1
        else:
            return 0

    @staticmethod
    def calculate_trending(is_rsi_uptrending, is_perfect_order, is_above_short_ma, is_above_middle_ma):
        if is_rsi_uptrending is None:
            return np.sum([is_perfect_order, is_above_short_ma, is_above_middle_ma])
        else:
            return np.sum([is_rsi_uptrending, is_perfect_order, is_above_short_ma, is_above_middle_ma])
        
    def next(self):
        if self.rsi_1W[-1] <= self.RSI_lower_threshold:
            self.is_rsi_up_trending = True      
        elif self.rsi_1W[-1] >= self.RSI_upper_threshold:
            self.is_rsi_up_trending = False
            
        is_perfect_order = self.is_perfect_order(self.sma_14W[-1], self.sma_21W[-1], self.sma_35W[-1])
        is_above_short_ma = self.data.Close[-1] >= self.sma_14W[-1]
        is_above_middle_ma = self.data.Close[-1] >= self.sma_21W[-1]
        
        trending = self.calculate_trending(self.is_rsi_up_trending, is_perfect_order, is_above_short_ma, is_above_middle_ma)

        if trending >= 3:
            # up trending
            if self.rsi_1D[-1] <= self.RSI_lower_threshold and self.rsi_4H[-1] <= self.RSI_lower_threshold:
                for trade in self.trades:
                    if trade.is_short:
                        trade.close()
                self.buy()

        elif trending == 0:
            # down trending
            if self.rsi_1D[-1] >= self.RSI_upper_threshold and self.rsi_4H[-1] >= self.RSI_upper_threshold:
                for trade in self.trades:
                    if trade.is_long:
                        trade.close()
                self.sell()    

class RSILongOnly(RSI):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.strategy_name = 'RSILongOnly'

    def next(self):
        if self.data._Data__i < self.RSI_shifter:
            return

        if self.rsi[-self.RSI_shifter] >= self.RSI_upper_threshold:
            self.position.close()
        elif self.rsi[-self.RSI_shifter] <= self.RSI_lower_threshold:
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
        if self.data._Data__i < self.RSI_shifter:
            return

        rsi_avg = self.rsi[-14:].mean()
        if self.rsi[-self.RSI_shifter] >= self.RSI_upper_threshold and self.rsi[-self.RSI_shifter] < rsi_avg:
            self.position.close()
            self.sell()
        elif self.rsi[-self.RSI_shifter] <= self.RSI_lower_threshold and self.rsi[-self.RSI_shifter] > rsi_avg:
            self.position.close()
            self.buy()

class ConnorsRSI(BaseStrategy):
    def __init__(self, broker, data, params):
        self.ConnorsRSI_shifter = 1
        self.ConnorsRSI_timeperiod = 3
        self.ConnorsRSI_count = 2
        self.ConnorsRSI_percentage_rank = 100
        self.ConnorsRSI_lower_threshold = 10
        self.ConnorsRSI_upper_threshold = 90
        self.set_optimization_parameter(
            ConnorsRSI_shifter=range(1, 10),
            ConnorsRSI_timeperiod=range(3, 10, 1),
            ConnorsRSI_count=range(2, 10, 1),
            ConnorsRSI_percentage_rank=range(90, 110, 5),
            ConnorsRSI_lower_threshold=range(5, 20, 5),
            ConnorsRSI_upper_threshold=range(80, 95, 5)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'ConnorsRSI'

    def init(self):
        super().init()
        self.rsi = self.metrics.CONNORSRSI(
            self.data, self.df_freq, self.ConnorsRSI_timeperiod, self.ConnorsRSI_count, self.ConnorsRSI_percentage_rank)

    def next(self):
        super().next()
        if self.data._Data__i < self.ConnorsRSI_shifter:
            return

        if self.rsi[-self.ConnorsRSI_shifter] >= self.ConnorsRSI_upper_threshold:
            self.position.close()
            self.sell()
        elif self.rsi[-self.ConnorsRSI_shifter] <= self.ConnorsRSI_lower_threshold:
            self.position.close()
            self.buy()

