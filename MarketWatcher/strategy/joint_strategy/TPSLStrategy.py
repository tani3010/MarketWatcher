# -*- coding: utf-8 -*-

from .JointStrategy import JointStrategy
from strategy.single_strategy.ChannelBreakOut import ChannelBreakOut
from strategy.single_strategy.TakeProfit import TakeProfit
from strategy.single_strategy.StopLoss import StopLoss
from strategy.single_strategy.PerfectOrder import PerfectOrder
from strategy.single_strategy.RSI import RSILongOnly, ConnorsRSI
from strategy.single_strategy.Trailing import Trailing

from logging import getLogger
logger = getLogger(__name__)

class ChannelBreakOutTakeProfit(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ChannelBreakOut, TakeProfit]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ChannelBreakOutTakeProfit'

class ChannelBreakOutStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ChannelBreakOut, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ChannelBreakOutStopLoss'

class ChannelBreakOutTakeProfitStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ChannelBreakOut, TakeProfit, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ChannelBreakOutTakeProfitStopLoss'

class PerfectOrderTakeProfit(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[PerfectOrder, TakeProfit]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PerfectOrderTakeProfit'

class PerfectOrderStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[PerfectOrder, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PerfectOrderStopLoss'

class PerfectOrderTakeProfitStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[PerfectOrder, TakeProfit, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PerfectOrderTakeProfitStopLoss'

class RSILongOnlyTakeProfit(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSILongOnly, TakeProfit]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'RSILongOnlyTakeProfit'

class RSILongOnlyTrailing(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSILongOnly, Trailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'RSILongOnlyTrailing'

class RSILongOnlyStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSILongOnly, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'RSILongOnlyStopLoss'

class RSILongOnlyTakeProfitStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSILongOnly, TakeProfit, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'RSILongOnlyTakeProfitStopLoss'

class ConnorsRSITakeProfit(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ConnorsRSI, TakeProfit]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ConnorsRSITakeProfit'

class ConnorsRSIStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ConnorsRSI, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ConnorsRSIStopLoss'

class ConnorsRSITakeProfitStopLoss(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ConnorsRSI, TakeProfit, StopLoss]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'ConnorsRSITakeProfitStopLoss'