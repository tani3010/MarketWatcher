# -*- coding: utf-8 -*-

import ccxt
from logging import getLogger
logger = getLogger(__name__)

class BaseTrader(object):
    def __init__(self, exchange, dict_credential=None):
        self.private_mode = False
        self.dict_credential = dict_credential
        if type(dict_credential) is dict and 'apiKey' in dict_credential.keys() and 'secret' in dict_credential.keys():
            self.exchange = eval('ccxt.' + exchange + '(dict_credential)')
            self.private_mode = True
        else:
            self.exchange = eval('ccxt.' + exchange + '()')
        self.exchange_name = self.exchange.id
        self.exchange.load_markets()

    def __del__(self):
        self.dict_credential = None

    def import_credential(self, dict_credential=None):
        self.__init__(self.exchange_name, dict_credential)

    @staticmethod
    def copy_dict(src_dict, dest_dict):
        for key, value in src_dict.items():
            dest_dict[key] = value
    
    def send_order(self, result, symbol, price, amount, is_buy, is_market=False, is_post_only=True, params={}):
        ret = False
        try:
            tmp_result = {}
            if is_market:
                if is_buy:
                    tmp_result = self.exchange.create_market_buy_order(symbol, amount, params)
                else:
                    tmp_result = self.exchange.create_market_sell_order(symbol, amount, params)
            else:
                if is_buy:
                    tmp_result = self.exchange.create_limit_buy_order(symbol, amount, price, params)
                else:
                    tmp_result = self.exchange.create_limit_sell_order(symbol, amount, price, params)
            self.copy_dict(tmp_result, result)
            ret = True
            logger.info('completed.')
        except Exception as e:
            logger.error(e.args)
            logger.warning('failed.')
        finally:
            return ret

    def cancel_order(self, result):
        pass

    def fetch_market_info(self):
        try:
            return self.exchange.fetch_markets()
        except Exception as e:
            logger.error(e.args)

    def fetch_symbol(self):
        return [x['symbol'] for x in self.fetch_market_info() if x['active']]

    def fetch_open_orders(self, symbol):
        try:
            return self.exchange.fetch_open_orders(symbol)
        except Exception as e:
            logger.error(e.args)

    def fetch_balance(self, result):
        ret = False
        try:
            tmp_result = self.exchange.fetch_balance()
            self.copy_dict(tmp_result, result)
            ret = True
            logger.info('completed.')
        except Exception as e:
            logger.error(e.args)
            logger.warning('failed.')
        finally:
            return ret

    def fetch_fee(self, result, symbol, price, amount, taker_or_maker='taker', params={}):
        ret = False
        try:
            type_ = None  # this is not used in public API
            side = None  # this is not used in public API
            tmp_result = self.exchange.calculate_fee(symbol, type_, side, amount, price, taker_or_maker, params)
            self.copy_dict(tmp_result, result)
            ret = True
            logger.info('completed.')
        except Exception as e:
            logger.error(e.args)
            logger.warning('failed.')
        finally:
            return ret

    def send_buy_order_market(self, result, symbol, price, amount, params={}):
        return self.send_order(result, symbol, price, amount, True, True, params)

    def send_sell_order_market(self, result, symbol, price, amount, params={}):
        return self.send_order(result, symbol, price, amount, False, True, params)

    def send_buy_order_limit(self, result, symbol, price, amount, is_post_only=True, params={}):
        return self.send_order(result, symbol, price, amount, True, False, is_post_only, params)

    def send_sell_order_limit(self, result, symbol, price, amount, is_post_only=True, params={}):
        return self.send_order(result, symbol, price, amount, False, False, is_post_only, params)

    def calculate_tradable_amount(self, result, symbol, price, side, type_, taker_or_maker='taker', safe_margin=0.005):
        ret = False
        result_balance = None
        result_fee = None
        if not self.fetch_balance(result_balance):
            logger.warning('fetch_balance: failed.')
            return ret

        if not self.fetch_fee(result_fee):
            logger.warning('fetch_fee: failed.')
            return ret

        tmp_result = result_balance / (price * result_fee) * (1 - safe_margin)
        self.copy_dict(tmp_result, result)
        ret = True
        return ret