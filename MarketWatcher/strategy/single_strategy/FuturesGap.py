# -*- coding: utf-8 -*-

import pandas as pd
from .BaseStrategy import BaseStrategy
from database.CommitmentsOfTradersLongFormatTableManager import CommitmentsOfTradersLongFormatTableManager
from backtesting.lib import crossover
from logging import getLogger
logger = getLogger(__name__)

class FuturesGap(BaseStrategy):
    def __init__(self, broker, data, params):
        self.FuturesGap_min_gap_level = 100
        self.set_optimization_parameter(
            FuturesGap_min_gap_level=range(50, 150, 10)
        )
        super().__init__(broker, data, params)
        self.strategy_name = 'FuturesGap'

    def init(self):
        super().init()

    def next(self):
        super().next()

        #if len(self.trades) > 0:
        #    return

        if self.data.index[-1].isoweekday() == 1 and self.data.index[-2].isoweekday() == 5:
            gap = self.data.Open[-1] - self.data.Close[-2]
            if gap >= self.FuturesGap_min_gap_level:
                #self.position.close()
                self.sell()
            elif gap <= -self.FuturesGap_min_gap_level:
                #self.position.close()
                self.buy()
 
class CommitmentOfTradersImbalance(BaseStrategy):
    def __init__(self, broker, data, params):
        self.set_optimization_parameter()
        super().__init__(broker, data, params)
        self.strategy_name = 'CommitmentOfTradersImbalance'
        self.pre_load()

    def pre_load(self):
        self.mgr = CommitmentsOfTradersLongFormatTableManager()

        df_price = self.data.df.copy(True)
        df_price.columns = pd.MultiIndex.from_arrays(
            [df_price.columns.values, df_price.columns.values, df_price.columns.values]
        )

        self.df_cot_summary = self.mgr.get_summary()
        self.df_cot_summary = self.df_cot_summary.merge(df_price, how='right', left_index=True, right_index=True)

    def init(self):
        super().init()
        self.df_cot_btc_lev_ratio = self.metrics.dummy(
            self.df_cot_summary, '1D',
            [('Lev_Long_Ratio', 'Combined', 'BTC+uBTC'), ('Lev_Short_Ratio', 'Combined', 'BTC+uBTC')],            
            name='cot_lev_ratio',)

        self.df_cot_btc_all_ratio = self.metrics.dummy(
            self.df_cot_summary, '1D',
            [('All_Long_Ratio', 'Combined', 'BTC+uBTC'), ('All_Short_Ratio', 'Combined', 'BTC+uBTC')],            
            name='cot_all_ratio',)

        self.df_cot_btc_all = self.metrics.dummy(
            self.df_cot_summary, '1D',
            [('All_Long_OI', 'Combined', 'BTC+uBTC'), ('All_Short_OI', 'Combined', 'BTC+uBTC'), ('All_OI', 'Combined', 'BTC+uBTC')],            
            'long', 'short', 'total', name='cot_all',)

        self.df_cot_btc_lev = self.metrics.dummy(
            self.df_cot_summary, '1D',
            [('Lev_Long_OI', 'Combined', 'BTC+uBTC'), ('Lev_Short_OI', 'Combined', 'BTC+uBTC'), ('Lev_OI', 'Combined', 'BTC+uBTC')],
            name='cot_lev',
            long='long', short='short', total='total')

    def next(self):
        super().next()