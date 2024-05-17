# -*- coding: utf-8 -*-

from .JointStrategy import JointStrategy
from strategy.single_strategy.GoldenCross import GoldenCross
from strategy.single_strategy.DeadCross import DeadCross
from strategy.single_strategy.Trailing import Trailing, PercentageTrailing
from strategy.single_strategy.RSI import RSI, ModifiedRSI
from strategy.single_strategy.WilliamsFractal import WilliamsFractal
from strategy.single_strategy.BuyTheDips import BuyTheDips
from strategy.single_strategy.SellTheRips import SellTheRips

from logging import getLogger
logger = getLogger(__name__)

class TrailingRSI(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSI, Trailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'TrailingRSI'

class TrailingModifiedRSI(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ModifiedRSI, Trailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'TrailingModifiedRSI'

class PercentageTrailingRSI(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[RSI, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingRSI'

class PercentageTrailingModifiedRSI(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[ModifiedRSI, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingModifiedRSI'

class PercentageTrailingWilliamsFractal(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[WilliamsFractal, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingWilliamsFractal'

class PercentageTrailingGoldenCross(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[GoldenCross, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingGoldenCross'

class PercentageTrailingDeadCross(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[DeadCross, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingDeadCross'

class PercentageTrailingGoldenDeadCross(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[GoldenCross, DeadCross, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingGoldenDeadCross'

class PercentageTrailingBuyTheDipsSellTheRips(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[BuyTheDips, SellTheRips, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingBuyTheDipsSellTheRips'

class PercentageTrailingBuyTheDips(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[BuyTheDips, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingBuyTheDips'

class PercentageTrailingSellTheRips(JointStrategy):
    def __init__(self, broker, data, params, strategy_list=[SellTheRips, PercentageTrailing]):
        super().__init__(broker, data, params, strategy_list)
        self.strategy_name = 'PercentageTrailingSellTheRips'
