# -*- coding,  utf-8 -*-

from .BaseDataBaseTableManager import BaseDataBaseTableManager

class FXTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_FX (
                datetime TEXT,
                updatetime NUMERIC,
                source TEXT,
                from_currency TEXT,
                to_currency TEXT,
                fx REAL,
                PRIMARY KEY (
                    datetime,
                    source,
                    from_currency,
                    to_currency
                )
            )
        """

        self.sql_insert = """
            INSERT OR IGNORE INTO TBL_FX (
                datetime,
                updatetime,
                source,
                from_currency,
                to_currency,
                fx
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        self.create_table()
