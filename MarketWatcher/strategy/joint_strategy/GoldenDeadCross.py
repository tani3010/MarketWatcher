# -*- coding: utf-8 -*-

from .JointStrategy import JointStrategy
from strategy.single_strategy.GoldenCross import GoldenCross
from strategy.single_strategy.DeadCross import DeadCross
from strategy.single_strategy.Trailing import Trailing

from logging import getLogger
logger = getLogger(__name__)

class GoldenDeadCross(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[GoldenCross, DeadCross]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'GoldenDeadCross'

class GoldenDeadCrossTrailing(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[GoldenCross, DeadCross, Trailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'GoldenDeadCrossTrailing'
