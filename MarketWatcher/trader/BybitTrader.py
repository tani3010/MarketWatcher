# -*- coding: utf-8 -*-

from .BaseTrader import BaseTrader
from logging import getLogger
logger = getLogger(__name__)

class BybitTrader(BaseTrader):
    def __init__(self, dict_credential=None):
        super().__init__('bybit', dict_credential)
