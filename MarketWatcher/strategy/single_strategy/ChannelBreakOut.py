# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy
from logging import getLogger
logger = getLogger(__name__)

class ChannelBreakOut(BaseStrategy):
    def __init__(self, broker, data, params):
        self.ChannelBreakOut_timeperiod = 5
        self.ChannelBreakOut_bandwidth = 1.6
        self.buy_position = False
        self.sell_position  = False
        self.set_optimization_parameter(
            ChannelBreakOut_timeperiod=range(3, 10, 1),
            ChannelBreakOut_bandwidth=[0.25*x for x in range(2, 12, 1)]
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'ChannelBreakOut'

    def calc_buy_price(self, timeperiod, bandwidth):
        sum_high = self.data.df['High'].rolling(timeperiod).sum() 
        sum_low = self.data.df['Low'].rolling(timeperiod).sum()
        return self.data['Open'] + ((sum_high - sum_low) / timeperiod)*bandwidth

    def calc_sell_price(self, timeperiod, bandwidth):
        sum_high = self.data.df['High'].rolling(timeperiod).sum() 
        sum_low = self.data.df['Low'].rolling(timeperiod).sum()
        return self.data['Open'] - ((sum_high - sum_low) / timeperiod)*bandwidth

    def init(self):
        super().init()
        self.price_buy = self.I(
            self.calc_buy_price, self.ChannelBreakOut_timeperiod,
            self.ChannelBreakOut_bandwidth, name='buy price({}, {})')
        self.price_sell = self.I(
            self.calc_sell_price, self.ChannelBreakOut_timeperiod,
            self.ChannelBreakOut_bandwidth, name='sell price({}, {})')

    def next(self):
        super().next()
        if (not self.buy_position) and (self.data.High[-1] > self.price_buy[-2]):
            self.position.close()
            self.buy()
            self.buy_position = True
            self.sell_position = False
        elif (not self.sell_position) and (self.data.Low[-1] < self.price_sell[-2]):
            self.position.close()
            self.sell()
            self.buy_position = False
            self.sell_position = True
