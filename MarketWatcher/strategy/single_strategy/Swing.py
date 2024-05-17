# -*- coding: utf-8 -*-

from .BaseStrategy import BaseStrategy

from logging import getLogger
logger = getLogger(__name__)

class Swing(BaseStrategy):
    def __init__(self):
        super().__init__()
        self._strategy_name = 'Swing'