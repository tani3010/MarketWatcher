# -*- coding: utf-8 -*-

from strategy.single_strategy.BaseStrategy import BaseStrategy
from backtesting._util import _Indicator
from logging import getLogger
logger = getLogger(__name__)

class JointStrategy(BaseStrategy):
    def __init__(self, broker, data, params, strategy_list):
        super().__init__(broker, data, params)
        self.strategy_name = 'JointStrategy'
        self.strategy_list = [strat(broker, data, params) for strat in strategy_list]
        self.strategy_name_list = [strat.strategy_name for strat in self.strategy_list]
        self.indicator_name_list = []
        self.parameters = {}
        self.optimization_parameter = {}

        for strat in self.strategy_list:
            for key, val in vars(strat).items():
                if key[0] != '_' and key not in ['metrics', 'strategy_name']:
                    setattr(self, key, val)
                    self.parameters[key] = val

        for strat in self.strategy_list:
            for key, val in self.parameters.items():
                if key not in vars(strat).keys():
                    setattr(strat, key, val)

            for key, val in strat.optimization_parameter.items():
                if key not in self.optimization_parameter:
                    self.optimization_parameter[key] = val

    def init(self):
        super().init()
        for strat in self.strategy_list:
            strat.init()
            for attr, indicator in strat.__dict__.items():
                if isinstance(indicator, _Indicator):
                    setattr(self, attr, indicator)
                    if indicator.name not in self.indicator_name_list:
                        self.indicator_name_list.append(indicator.name)
                        self._indicators.append(indicator)

    def setattr_children(self):
        for attr, indicator in self.__dict__.items():
            if isinstance(indicator, _Indicator):
                for strat in self.strategy_list:
                    if attr in strat.__dict__.keys():
                        setattr(strat, attr, indicator)

    def next(self):
        super().next()
        self.setattr_children()
        for strat in self.strategy_list:
            strat.next()

    def get_used_parameter(self):
        output_dict = {}
        for strat in self.strategy_list:
            _dict = strat.get_used_parameter()
            output_dict.update(_dict)
        return output_dict