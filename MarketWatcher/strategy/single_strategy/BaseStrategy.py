# -*- coding: utf-8 -*-

import pandas as pd
from backtesting import Strategy
from metrics.Metrics import Metrics
from logging import getLogger
logger = getLogger(__name__)

class BaseStrategy(Strategy):
    def __init__(self, broker, data, params):
        safe_params = self.get_safe_params(params)
        super().__init__(broker, data, safe_params)
        self.metrics = Metrics()
        self.strategy_name = 'BaseStrategy'
        self.df_freq = self.data.df.index.inferred_freq
        # self.optimization_parameter = {}
        if self.df_freq is None:
            self.df_freq = '1D'

    def init(self):
        super().init()

    def get_safe_params(self, params):
        safe_params = params.copy()
        for key, val in params.items():
            if key not in self.__dict__.keys():
                del safe_params[key]
        return safe_params

    def set_optimization_parameter(self, **kwargs):
        if hasattr(self, 'optimization_parameter'):
            for key, val in kwargs.items():
                if not key in self.optimization_parameter:
                    self.optimization_parameter[key] = val
        else:
            self.optimization_parameter = kwargs

    def get_optimization_parameter(self):
        return self.optimization_parameter

    def get_used_parameter(self):
        if not 'optimization_parameter' in self.__dict__:
            return {}
        output_dict = {key: val for key, val in self.__dict__.items() if key in self.__dict__['optimization_parameter'].keys()}
        tmp_dict = {key: val for key, val in self.__dict__.items() if key.startswith(self.strategy_name + '_')}
        output_dict.update(tmp_dict)
        return output_dict

    def infer_freq(self):
        pass