# -*- coding: utf-8 -*-

import os
import pandas as pd
import yfinance as yf

from .APIManager import APIManager
from database.OHLCVTableManager import OHLCVTableManager

from logging import getLogger
logger = getLogger(__name__)

class OHLCVAPIManager(APIManager):
    def __init__(self):
        super().__init__()

        self.table_dtypes = {
            'product_code': str,
            'datetime': str,
            'Open': float,
            'Close': float,
            'High': float,
            'Low': float,
            'Volume': float,
            'Change': float
        }

        self.table_header = [
            'timestamp',
            'updatetime',
            'datetime',
            'exchange',
            'product_code',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Change',
            'source'
        ]

    def get_catalog(self):
        self.load_yaml()
        for key, val in self.yaml['MarketSetting'].items():
            if 'apiCatalog' in val.keys():
                df = self.request_dataframe(val['apiCatalog'], 'data')
        return df

    def update_db(self):
        db = OHLCVTableManager()

        # update yahoo OHLCV
        try:
            df_yahoo = self.get_ohlcv_yahoo()
            df_yahoo = db.get_safe_OHLCV(df_yahoo)
            db.insert_many(df_yahoo.values)

            df_yahoo = self.get_ohlcv_yahoo2()
            df_yahoo = db.get_safe_OHLCV(df_yahoo)
            db.insert_many(df_yahoo.values)
        except Exception as e:
            logger.error('[yahoo finance] updating OHLCV failed.')
            logger.error(e.args)

        # update OHLCV
        try:
            df = self.get_ohlcv()
            db.insert_many(df.values)
        except Exception as e:
            logger.error('[api OHLCV] updating OHLCV failed.')
            logger.error(e.args)

    def get_ohlcv(self):
        self.load_yaml()
        df = None
        for exc in self.yaml['MarketSetting'].values():
            if not exc['valid']:
                continue

            for timebar in exc['defaultTimeBar']:
                for prd_key, prd_val in exc['products'].items():
                    self.base_url = exc['apiBaseURL']
                    for inst in prd_val:
                        try:
                            output = self.request_suburl(exc['historicalDataApi'].format(prd_key, inst, timebar))
                            if 'historicalDataDFKeys' in exc.keys():
                                tmp = output
                                for key in exc['historicalDataDFKeys']:
                                    tmp = tmp[key.format(prd_key)]
                                output = tmp

                            if isinstance(output, dict):
                                tmpdf = pd.DataFrame(output, index=[0])
                            else:
                                if 'defaultHistoricalDataColumns' in exc.keys():
                                    tmpdf = pd.DataFrame(output, columns=exc['defaultHistoricalDataColumns'])
                                else:
                                    tmpdf = pd.DataFrame(output)

                            if 'ohlcvHeader' in exc.keys():
                                tmpdf.rename(columns=exc['ohlcvHeader'], inplace=True)

                            tmpdf = self.add_column(tmpdf, 'exchange', prd_key)
                            tmpdf = self.add_column(tmpdf, 'product_code', inst.upper())
                            tmpdf = self.add_column(tmpdf, 'Change', 0.0)
                            tmpdf = self.convert_dtypes(tmpdf, self.table_dtypes)
                            tmpdf = self.add_timestamp_datetime(tmpdf)
                            tmpdf = self.add_updatetime(tmpdf)
                            df = tmpdf if df is None else df.merge(tmpdf, how='outer')
                            logger.info('[{}][{}][{}{}] api connection completed.'.format(
                                prd_key,
                                inst,
                                self.base_url,
                                exc['historicalDataApi'].format(prd_key, inst, timebar)))
                        except Exception as e:
                            logger.error('[{}][{}][{}{}] api connection failed.'.format(
                                prd_key,
                                inst,
                                self.base_url,
                                exc['historicalDataApi'].format(prd_key, inst, timebar)))
        df = df[df.Close > 0]
        df['source'] = ''
        df = df[self.table_header]
        return df

    def get_ohlcv_yahoo(self):
        self.load_yaml()
        api_url_format = self.yaml['MarketSetting_yahoo']['apiBaseURL'] + self.yaml['MarketSetting_yahoo']['historicalDataApi']
        df = None

        db = OHLCVTableManager()
        dict_exchange = db.fetch_symbols(as_dict=True)
        for prd in self.yaml['MarketSetting_yahoo']['products']:
            try:
                ticker_info = dict_exchange
                exchange_name = ''
                api_url = api_url_format.format(prd)
                ticker = yf.Ticker(prd)
                ticker_df = ticker.history(period='60d', interval='1d')
                # ticker_df = ticker.history(period='max', interval='1d')
                if prd in dict_exchange.keys():
                    exchange_name = ticker_info[prd]
                else:
                    ticker_info = ticker.get_info()
                    exchange_name = ticker_info['exchange']
                ticker_df['datetime'] = ticker_df.index
                ticker_df = self.add_column(ticker_df, 'exchange', exchange_name)
                ticker_df = self.add_column(ticker_df, 'product_code', prd)
                ticker_df = self.add_column(ticker_df, 'Change', 0.0)
                ticker_df = self.convert_dtypes(ticker_df, self.table_dtypes)
                ticker_df = self.add_timestamp_datetime(ticker_df)
                ticker_df = self.add_updatetime(ticker_df)
                df = ticker_df if df is None else df.merge(ticker_df, how='outer')
                logger.info('[yahoo finance][{}][{}] api connection completed.'.format(prd, api_url))
            except Exception as e:
                logger.error('[yahoo finance][{}][{}] api connection failed.'.format(prd, api_url))
                logger.error(e.args)

        df = df[df.Close > 0]
        df['source'] = ''
        df = df[self.table_header]
        return df

    # temporary data due to coinmetrics fail
    def get_ohlcv_yahoo2(self):
        target_dict = {
            'ETH-USD': [
                ['coinbase', 'ETH-USD-SPOT'],
                ['bybit', 'ETHUSD-FUTURE'],
                ['bitmex', 'ETHUSD-FUTURE'],
                ['binance', 'ETHUSD_PERP-FUTURE']
            ],
            'BTC-USD': [
                ['coinbase', 'BTC-USD-SPOT'],
                ['bybit', 'BTCUSD-FUTURE'],
                ['bitmex', 'XBTUSD-FUTURE'],
                ['binance', 'BTCUSD_PERP-FUTURE']
            ],
            'XRP-USD' : [
                ['bybit', 'XRPUSD-FUTURE'],
                ['bitmex', 'XRPUSD-FUTURE'],
                ['binance', 'XRPUSD_PERP-FUTURE']
            ],
            'BTC-JPY': [
                ['bitflyer', 'BTC-JPY-SPOT']
            ],
            'ETH-JPY': [
                ['bitflyer', 'ETH-JPY-SPOT']
            ],
            'XRP-JPY': [
                ['bitflyer', 'XRP-JPY-SPOT']
            ]
        }

        df = pd.DataFrame()
        for key, val in target_dict.items():
            tickerData = yf.Ticker(key)
            tmp_df = tickerData.history(period='60d', interval='5m')
            for x in val:
                try:
                    ticker_df = tmp_df.copy(deep=True)
                    ticker_df['datetime'] = ticker_df.index
                    ticker_df = self.add_column(ticker_df, 'exchange', x[0])
                    ticker_df = self.add_column(ticker_df, 'product_code', x[1])
                    ticker_df = self.add_column(ticker_df, 'Change', 0.0)
                    ticker_df = self.convert_dtypes(ticker_df, self.table_dtypes)
                    df = pd.concat([df, ticker_df], ignore_index=False)
                    logger.info('[yahoo finance][{}][{}] api connection completed.'.format(x[0], x[1]))
                except Exception as e:
                    logger.error('[yahoo finance][{}][{}] api connection failed.'.format(x[0], x[1]))
                    logger.error(e.args)

        df = self.add_timestamp_datetime(df)
        df = self.add_updatetime(df)
        df['source'] = 'alternative'
        df['Volume'] = 0.0
        df = df[df.Close > 0]
        df = df[self.table_header]
        df = df[df.index > '2025/10/26 00:00']  # data missing from

        return df