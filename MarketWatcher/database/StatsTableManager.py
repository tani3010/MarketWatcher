# -*- coding,  utf-8 -*-

from .BaseDataBaseTableManager import BaseDataBaseTableManager

class StatsTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('TRADE.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_STATS (
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
                duration TEXT,
                exposure_time REAL,
                equity_initial REAL,
                equity_final REAL,
                equity_peak REAL,
                return REAL,
                buyandhold_return REAL,
                return_ann REAL,
                volatility_ann REAL,
                sharpe_ratio REAL,
                sortino_ratio REAL,
                calmar_ratio REAL,
                max_drawdown REAL,
                avg_drawdown REAL,
                max_drawdown_duration TEXT,
                avg_drawdown_duration TEXT,
                trade_num REAL,
                win_rate REAL,
                best_trade REAL,
                worst_trade REAL,
                avg_trade REAL,
                max_trade_duration TEXT,
                avg_trade_duration TEXT,
                profit_factor REAL,
                expectancy REAL,
                SQN REAL,
                kelly_criterion REAL,
                parameter TEXT,
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
            INSERT OR IGNORE INTO TBL_STATS (
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
                duration,
                exposure_time,
                equity_initial,
                equity_final,
                equity_peak,
                return,
                buyandhold_return,
                return_ann,
                volatility_ann,
                sharpe_ratio,
                sortino_ratio,
                calmar_ratio,
                max_drawdown,
                avg_drawdown,
                max_drawdown_duration,
                avg_drawdown_duration,
                trade_num,
                win_rate,
                best_trade,
                worst_trade,
                avg_trade,
                max_trade_duration,
                avg_trade_duration,
                profit_factor,
                expectancy,
                SQN,
                kelly_criterion,
                parameter
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.create_table()