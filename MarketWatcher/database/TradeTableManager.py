# -*- coding,  utf-8 -*-

from .BaseDataBaseTableManager import BaseDataBaseTableManager

class TradeTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('TRADE.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_TRADE (
                updatetime NUMERIC,
                datetime TEXT,
                strategy_name TEXT,
                exchange TEXT,
                product_code TEXT,
                freq TEXT,
                optimized INT,
                test_type TEXT,
                starttime TEXT,
                endtime TEXT,
                size REAL,
                entry_bar REAL,
                exit_ar REAL,
                entry_price REAL,
                exit_price REAL,
                pnl REAL,
                return_pct REAL,
                entrytime TEXT,
                exittime TEXT,
                tag TEXT,
                duration TEXT,
                PRIMARY KEY (
                    datetime,
                    strategy_name,
                    starttime,
                    endtime,
                    exchange,
                    product_code,
                    freq,
                    optimized,
                    test_type
                )
            )
        """

        self.sql_insert = """
            INSERT OR IGNORE INTO TBL_TRADE (
                updatetime,
                datetime,
                strategy_name,
                exchange,
                product_code,
                freq,
                optimized,
                test_type,
                starttime,
                endtime,
                size,
                entry_bar,
                exit_bar,
                entry_price,
                exit_price,
                pnl,
                return_pct,
                entrytime,
                exittime,
                tag,
                duration
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.create_table()