# -*- coding,  utf-8 -*-

from .BaseDataBaseTableManager import BaseDataBaseTableManager

class FundingRateTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_FUNDINGRATE (
                timestamp NUMERIC,
                updatetime NUMERIC,
                datetime TEXT,
                exchange TEXT,
                product_code TEXT,
                funding_rate REAL,
                PRIMARY KEY (
                    timestamp,
                    exchange,
                    product_code
                )
            )
        """

        self.sql_insert = """
            INSERT OR IGNORE INTO TBL_FUNDINGRATE (
                timestamp,
                updatetime,
                datetime,
                exchange,
                product_code,
                funding_rate
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        self.create_table()

    def fetch_funding_rate(self, exchange, product_code):
        sql = '''
            select
              *
            from
              TBL_FUNDINGRATE
            where
              exchange = '{}'
              and product_code = '{}'
            order by
              datetime
        '''.format(exchange, product_code)
        df = self.select(sql, True, True)
        df = self.set_datetime_as_index(df)
        return df

class FundingRateMonthlyTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_FUNDINGRATE_MONTHLY (
                timestamp TEXT,
                updatetime NUMERIC,
                exchange TEXT,
                product_code TEXT,
                funding_rate REAL,
                PRIMARY KEY (
                    timestamp,
                    exchange,
                    product_code
                )
            )
        """

        self.sql_insert = """
            INSERT INTO TBL_FUNDINGRATE_MONTHLY (
                timestamp,
                updatetime,
                exchange,
                product_code,
                funding_rate
            ) VALUES (?, ?, ?, ?, ?)
        """

        self.sql_upsert = """
            INSERT INTO TBL_FUNDINGRATE_MONTHLY (
                timestamp,
                updatetime,
                exchange,
                product_code,
                funding_rate
            )
            VALUES
                (?, ?, ?, ?, ?)
            ON CONFLICT
                (timestamp, exchange, product_code)
            DO UPDATE
                set
                    updatetime = excluded.updatetime,
                    funding_rate = excluded.funding_rate
        """

        self.create_table()

class FundingRateYearlyTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_FUNDINGRATE_YEARLY (
                timestamp TEXT,
                updatetime NUMERIC,
                exchange TEXT,
                product_code TEXT,
                funding_rate REAL,
                PRIMARY KEY (
                    timestamp,
                    exchange,
                    product_code
                )
            )
        """

        self.sql_insert = """
            INSERT INTO TBL_FUNDINGRATE_YEARLY (
                timestamp,
                updatetime,
                exchange,
                product_code,
                funding_rate
            ) VALUES (?, ?, ?, ?, ?)
        """

        self.sql_upsert = """
            INSERT INTO TBL_FUNDINGRATE_YEARLY (
                timestamp,
                updatetime,
                exchange,
                product_code,
                funding_rate
            )
            VALUES
                (?, ?, ?, ?, ?)
            ON CONFLICT
                (timestamp, exchange, product_code)
            DO UPDATE
                set
                    updatetime = excluded.updatetime,
                    funding_rate = excluded.funding_rate
        """

        self.create_table()

def fetch_funding_rate(exchange_name, product_code):
    db_mgr = FundingRateTableManager()
    df = db_mgr.fetch_funding_rate(exchange_name, product_code)
    return df
