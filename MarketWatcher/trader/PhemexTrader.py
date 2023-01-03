# -*- coding: utf-8 -*-

from .BaseTrader import BaseTrader
from logging import getLogger
logger = getLogger(__name__)

class PhemexTrader(BaseTrader):
    def __init__(self, dict_credential=None):
        super().__init__('phemex', dict_credential)

    def fetch_account_balance(self, currency):
        safe_currency = currency.upper()
        return self.exchange.private_get_accounts_accountpositions({'currency': safe_currency})

