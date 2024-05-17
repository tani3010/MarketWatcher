# -*- coding,  utf-8 -*-

import os
import pandas as pd
from .BaseDataBaseTableManager import BaseDataBaseTableManager

class OHLCVTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_OHLCV (
                timestamp NUMERIC,
                updatetime NUMERIC,
                datetime TEXT,
                exchange TEXT,
                product_code TEXT,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Volume REAL,
                Change REAL,
                source TEXT,
                PRIMARY KEY (
                    timestamp,
                    exchange,
                    product_code
                )
            )
        """

        self.sql_insert = """
            INSERT OR IGNORE INTO TBL_OHLCV (
                timestamp,
                updatetime,
                datetime,
                exchange,
                product_code,
                Open,
                High,
                Low,
                Close,
                Volume,
                Change,
                source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.sql_symbols = """
            SELECT DISTINCT
                exchange,
                product_code
            FROM
                TBL_OHLCV
            ORDER BY
              exchange,
              product_code
        """

        self.create_table()

    def resample(self, df, freq, drop_na=False, closed='right', label='right'):
        df = self.set_datetime_as_index(df)
        dict_ohlc = {
          'Open': 'first',
          'High': 'max',
          'Low': 'min',
          'Close': 'last',
          'Volume': 'sum'
        }
        df = df.resample(freq, closed=closed, label=label).agg(dict_ohlc)
        if drop_na:
            df = df.dropna()
        else:
            df = df.ffill()
        return df

    def fetch_OHLCV(self, exchange_name, symbol, freq=None, from_date='1950-01-01', to_date='2100-12-31', drop_na=False, closed='right', label='right'):
        sql = '''
        select
          datetime,
          Open,
          High,
          Low,
          Close,
          Volume
        from
          TBL_OHLCV
        where
          exchange = '{}'
          and product_code = '{}'
          and datetime >= '{}'
          and datetime <= '{}'
        order by
          datetime
        '''.format(exchange_name, symbol, from_date, to_date)
        df = self.select(sql, True, True)
        # df = self.get_safe_OHLCV(df)
        df = self.set_datetime_as_index(df)
        if freq is not None:
            df = self.resample(df, freq, drop_na, closed=closed, label=label)
        return df

    def fetch_symbols(self, as_dict=False):
        df = self.select(self.sql_symbols, True, True)
        if as_dict:
            df = dict(zip(df['product_code'], df['exchange']))
        return df

    @staticmethod
    def get_safe_OHLCV(df):
        if not 'Open' in df.columns:
            return df

        # missing Open
        for i, row in df.iterrows():
            if i >= 1 and (df.at[i, 'Open'] == 0 or df.at[i, 'Open'] is None):
                df.at[i, 'Open'] = df.at[i-1, 'Close']
        return df

    def export_ohlcv(self):
        df_symbol = self.select(self.sql_symbols, True, True)
        sql_ohlcv = "select * from TBL_OHLCV where (exchange='{}' and product_code in ('{}')) order by datetime"

        for idx, row in df_symbol.iterrows():
            sql_tmp = sql_ohlcv.format(row['exchange'], row['product_code'])
            df_tmp = self.select(sql_tmp, True, True)

            file_name = r'ohlcv_{}_{}.csv'.format(row['exchange'], row['product_code'])
            file_name = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', 'ohlcv', file_name))        
            df_tmp.to_csv(file_name, index=False)

    def export_ohlcv_stats(self):
        sql = '''
            SELECT distinct
              exchange
              , product_code
              , COUNT(*) as DATA_COUNT
              , min(datetime) AS DT_BEGIN
              , max(datetime) AS DT_END
            FROM
              TBL_OHLCV
            GROUP BY
              exchange, product_code
            ORDER BY
              exchange, product_code
        '''
        df = self.select(sql, True, True)
        return df

def fetch_OHLCV(exchange_name, symbol, freq=None, from_date='1950-01-01', to_date='2100-12-31', drop_na=False):
    db_mgr = OHLCVTableManager()
    df = db_mgr.fetch_OHLCV(exchange_name, symbol, freq, from_date, to_date, drop_na)
    return df

def fetch_symbols():
    db_mgr = OHLCVTableManager()
    df = db_mgr.fetch_symbols()
    return df

if __name__ == '__main__':
    df = fetch_symbols()
