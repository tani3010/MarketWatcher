# -*- coding: utf-8 -*-
import os
import pandas as pd
from datetime import datetime
from .APIManager import APIManager
from database.FundingRateTableManager import FundingRateTableManager, FundingRateMonthlyTableManager, FundingRateYearlyTableManager

from logging import getLogger
logger = getLogger(__name__)

class FundingRateAPIManager(APIManager):
    def __init__(self):
        super().__init__()
        self.table_dtypes = {
            'product_code': str,
            'datetime': str,
            'timestamp': float,
            'funding_rate': float
        }
        
        self.table_header = [
            'timestamp',
            'updatetime',
            'datetime',
            'exchange',
            'product_code',
            'funding_rate'
        ]

    def update_db(self):
        df = self.get_funding_rate()
        db = FundingRateTableManager()
        db.insert_many(df.values)

    def update_db_mexc(self):
        self.load_yaml()
        df = None
        output = []
        exc = self.yaml['ExchangeSetting']['mexc']
        for prd in exc['products']:
            page_num = 1
            total_page = 2000
            try:
                self.base_url = exc['apiBaseURL']
                while page_num <= total_page:
                    tmpurl = exc['fundingRateApi'].format(prd) + f'&page_num={page_num}'
                    _output = self.request_suburl(tmpurl)
                    total_page = _output['data']['totalPage']
                    if 'fundingRateDFKeys' in exc.keys():
                        tmp = _output
                        for key in exc['fundingRateDFKeys']:
                            tmp = tmp[key.format(prd)]
                        _output = tmp                    
                    page_num += 1
                    output.extend(_output)

                if isinstance(output, dict):
                    tmpdf = pd.DataFrame(output, index=[0])
                else:
                    tmpdf = pd.DataFrame(output)
                tmpdf.rename(columns=exc['fundingRateHeader'], inplace=True)
                tmpdf = self.add_column(tmpdf, 'exchange', exc['exchangeName'])
                tmpdf = self.add_column(tmpdf, 'product_code', prd)
                tmpdf = self.convert_dtypes(tmpdf, self.table_dtypes)
                tmpdf = self.add_timestamp_datetime(tmpdf)
                tmpdf = self.add_updatetime(tmpdf)
                df = tmpdf if df is None else df.merge(tmpdf, how='outer')
                logger.info('[{}][{}][{}{}] api connection completed.'.format(
                    exc['exchangeName'],
                    prd,
                    self.base_url,
                    exc['fundingRateApi'].format(prd)))
            except Exception as e:
                logger.error('[{}][{}][{}{}] api connection failed.'.format(
                    exc['exchangeName'],
                    prd,
                    self.base_url,
                    exc['fundingRateApi'].format(prd)))
        df = df[self.table_header]
        db = FundingRateTableManager()
        db.insert_many(df.values)

    def get_funding_rate(self):
        self.load_yaml()
        df = None
        for exc in self.yaml['ExchangeSetting'].values():
            if not exc['valid']:
                continue
            for prd in exc['products']:
                try:
                    self.base_url = exc['apiBaseURL']
                    output = self.request_suburl(exc['fundingRateApi'].format(prd))
                    if 'fundingRateDFKeys' in exc.keys():
                        tmp = output
                        for key in exc['fundingRateDFKeys']:
                            tmp = tmp[key.format(prd)]
                        output = tmp
                    if isinstance(output, dict):
                        tmpdf = pd.DataFrame(output, index=[0])
                    else:
                        tmpdf = pd.DataFrame(output)
                    tmpdf.rename(columns=exc['fundingRateHeader'], inplace=True)
                    tmpdf = self.add_column(tmpdf, 'exchange', exc['exchangeName'])
                    tmpdf = self.add_column(tmpdf, 'product_code', prd)
                    tmpdf = self.convert_dtypes(tmpdf, self.table_dtypes)
                    tmpdf = self.add_timestamp_datetime(tmpdf)
                    tmpdf = self.add_updatetime(tmpdf)
                    df = tmpdf if df is None else df.merge(tmpdf, how='outer')
                    logger.info('[{}][{}][{}{}] api connection completed.'.format(
                        exc['exchangeName'],
                        prd,
                        self.base_url,
                        exc['fundingRateApi'].format(prd)))
                except Exception as e:
                    logger.error('[{}][{}][{}{}] api connection failed.'.format(
                        exc['exchangeName'],
                        prd,
                        self.base_url,
                        exc['fundingRateApi'].format(prd)))
        df = df[self.table_header]
        return df

    @staticmethod
    def calc_funding_return(df, isMonthly=False):
        df_tmp = df.copy()
        df_tmp['tmpFundingRate'] = df.fundingRate + 1
        if isMonthly:
            df_tmp = (df_tmp.groupby(df.datetime.dt.strftime('%Y-%m')).tmpFundingRate.agg(['prod']) - 1)
        else:
            df_tmp = (df_tmp.groupby(df.datetime.dt.strftime('%Y')).tmpFundingRate.agg(['prod']) - 1)
        df_tmp = df_tmp.rename(columns={'prod': 'fundingRate'})
        df_tmp['exchange'] = df['exchange'][0]
        df_tmp['product_code'] = df['product_code'][0]
        return df_tmp

    def export_funding_summary(self):
        mgr = FundingRateTableManager()
        sql = 'SELECT * FROM TBL_FUNDINGRATE'
        dat = pd.DataFrame(mgr.select(sql),
            columns=['timestamp', 'updatetime', 'datetime', 'exchange', 'product_code', 'fundingRate'])
        dat['datetime'] = dat['timestamp'].map(lambda x: datetime.utcfromtimestamp(x))

        df_monthly = None
        df_yearly = None
        for ext in dat.exchange.unique():
            for symbol in dat.product_code.unique():
                df_tmp = dat[((dat['exchange'] == ext) & (dat['product_code'] == symbol))].sort_values('datetime')
                if not df_tmp.empty:
                    df_tmp = df_tmp.reset_index()
                    if df_monthly is None:
                        df_monthly = self.calc_funding_return(df_tmp, True)
                    else:
                        df_monthly = pd.concat([df_monthly, self.calc_funding_return(df_tmp, True)])

                    if df_yearly is None:
                        df_yearly = self.calc_funding_return(df_tmp, False)
                    else:
                        df_yearly = pd.concat([df_yearly, self.calc_funding_return(df_tmp, False)])

        self.output_funding_table()

        header = ['time', 'updatetime', 'exchange', 'product_code', 'fundingRate']
        df_monthly['time'] = df_monthly.index
        df_yearly['time'] = df_yearly.index
        
        df_monthly = self.add_updatetime(df_monthly)
        df_yearly = self.add_updatetime(df_yearly)

        mgr = FundingRateMonthlyTableManager()
        mgr.upsert_many(df_monthly[header].values)

        mgr = FundingRateYearlyTableManager()
        mgr.upsert_many(df_yearly[header].values)

    @staticmethod
    def output_funding_table():
        mgr = FundingRateTableManager()
        sql = 'SELECT * FROM {} ORDER BY timestamp DESC, funding_rate DESC'
        tables = ['TBL_FUNDINGRATE', 'TBL_FUNDINGRATE_MONTHLY', 'TBL_FUNDINGRATE_YEARLY']
        
        for tab in tables:
            sql_tmp = sql.format(tab)
            dat = mgr.select(sql_tmp, True)
            df = pd.DataFrame(dat[1:], columns=dat[0])
            output_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', '{}.csv'.format(tab)))
            df.to_csv(output_file, index=False)
        