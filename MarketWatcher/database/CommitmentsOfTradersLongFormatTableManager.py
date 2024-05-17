# -*- coding,  utf-8 -*-

from .BaseDataBaseTableManager import BaseDataBaseTableManager
import pandas as pd

class CommitmentsOfTradersLongFormatTableManager(BaseDataBaseTableManager):
    def __init__(self):
        super().__init__('MARKET.db')
        self.sql_create_table = """
            CREATE TABLE IF NOT EXISTS TBL_COMMITMENTSOFTRADERS_LONGFORMAT (
                Market_and_Exchange_Names TEXT,
                As_of_Date_in_Form_YYMMDD REAL,
                Report_Date_as_YYYY_MM_DD TEXT,
                CFTC_Contract_Market_Code REAL,
                CFTC_Market_Code_in_Initials TEXT,
                CFTC_Region_Code REAL,
                CFTC_Commodity_Code REAL,
                Open_Interest_All REAL,
                Noncommercial_Positions_Long_All REAL,
                Noncommercial_Positions_Short_All REAL,
                Noncommercial_Positions_Spreading_All REAL,
                Commercial_Positions_Long_All REAL,
                Commercial_Positions_Short_All REAL,
                Total_Reportable_Positions_Long_All REAL,
                Total_Reportable_Positions_Short_All REAL,
                Nonreportable_Positions_Long_All REAL,
                Nonreportable_Positions_Short_All REAL,
                Open_Interest_Old REAL,
                Noncommercial_Positions_Long_Old REAL,
                Noncommercial_Positions_Short_Old REAL,
                Noncommercial_Positions_Spreading_Old REAL,
                Commercial_Positions_Long_Old REAL,
                Commercial_Positions_Short_Old REAL,
                Total_Reportable_Positions_Long_Old REAL,
                Total_Reportable_Positions_Short_Old REAL,
                Nonreportable_Positions_Long_Old REAL,
                Nonreportable_Positions_Short_Old REAL,
                Open_Interest_Other REAL,
                Noncommercial_Positions_Long_Other REAL,
                Noncommercial_Positions_Short_Other REAL,
                Noncommercial_Positions_Spreading_Other REAL,
                Commercial_Positions_Long_Other REAL,
                Commercial_Positions_Short_Other REAL,
                Total_Reportable_Positions_Long_Other REAL,
                Total_Reportable_Positions_Short_Other REAL,
                Nonreportable_Positions_Long_Other REAL,
                Nonreportable_Positions_Short_Other REAL,
                Change_in_Open_Interest_All REAL,
                Change_in_Noncommercial_Long_All REAL,
                Change_in_Noncommercial_Short_All REAL,
                Change_in_Noncommercial_Spreading_All REAL,
                Change_in_Commercial_Long_All REAL,
                Change_in_Commercial_Short_All REAL,
                Change_in_Total_Reportable_Long_All REAL,
                Change_in_Total_Reportable_Short_All REAL,
                Change_in_Nonreportable_Long_All REAL,
                Change_in_Nonreportable_Short_All REAL,
                Pct_of_Open_Interest_OI_All REAL,
                Pct_of_OI_Noncommercial_Long_All REAL,
                Pct_of_OI_Noncommercial_Short_All REAL,
                Pct_of_OI_Noncommercial_Spreading_All REAL,
                Pct_of_OI_Commercial_Long_All REAL,
                Pct_of_OI_Commercial_Short_All REAL,
                Pct_of_OI_Total_Reportable_Long_All REAL,
                Pct_of_OI_Total_Reportable_Short_All REAL,
                Pct_of_OI_Nonreportable_Long_All REAL,
                Pct_of_OI_Nonreportable_Short_All REAL,
                Pct_of_Open_Interest_OIOld REAL,
                Pct_of_OI_Noncommercial_Long_Old REAL,
                Pct_of_OI_Noncommercial_Short_Old REAL,
                Pct_of_OI_Noncommercial_Spreading_Old REAL,
                Pct_of_OI_Commercial_Long_Old REAL,
                Pct_of_OI_Commercial_Short_Old REAL,
                Pct_of_OI_Total_Reportable_Long_Old REAL,
                Pct_of_OI_Total_Reportable_Short_Old REAL,
                Pct_of_OI_Nonreportable_Long_Old REAL,
                Pct_of_OI_Nonreportable_Short_Old REAL,
                Pct_of_Open_Interest_OI_Other REAL,
                Pct_of_OI_Noncommercial_Long_Other REAL,
                Pct_of_OI_Noncommercial_Short_Other REAL,
                Pct_of_OI_Noncommercial_Spreading_Other REAL,
                Pct_of_OI_Commercial_Long_Other REAL,
                Pct_of_OI_Commercial_Short_Other REAL,
                Pct_of_OI_Total_Reportable_Long_Other REAL,
                Pct_of_OI_Total_Reportable_Short_Other REAL,
                Pct_of_OI_Nonreportable_Long_Other REAL,
                Pct_of_OI_Nonreportable_Short_Other REAL,
                Traders_Total_All REAL,
                Traders_Noncommercial_Long_All REAL,
                Traders_Noncommercial_Short_All REAL,
                Traders_Noncommercial_Spreading_All REAL,
                Traders_Commercial_Long_All REAL,
                Traders_Commercial_Short_All REAL,
                Traders_Total_Reportable_Long_All REAL,
                Traders_Total_Reportable_Short_All REAL,
                Traders_Total_Old REAL,
                Traders_Noncommercial_Long_Old REAL,
                Traders_Noncommercial_Short_Old REAL,
                Traders_Noncommercial_Spreading_Old REAL,
                Traders_Commercial_Long_Old REAL,
                Traders_Commercial_Short_Old REAL,
                Traders_Total_Reportable_Long_Old REAL,
                Traders_Total_Reportable_Short_Old REAL,
                Traders_Total_Other REAL,
                Traders_Noncommercial_Long_Other REAL,
                Traders_Noncommercial_Short_Other REAL,
                Traders_Noncommercial_Spreading_Other REAL,
                Traders_Commercial_Long_Other REAL,
                Traders_Commercial_Short_Other REAL,
                Traders_Total_Reportable_Long_Other REAL,
                Traders_Total_Reportable_Short_Other REAL,
                Concentration_Gross_LT_4_TDR_Long_All REAL,
                Concentration_Gross_LT_4_TDR_Short_All REAL,
                Concentration_Gross_LT_8_TDR_Long_All REAL,
                Concentration_Gross_LT_8_TDR_Short_All REAL,
                Concentration_Net_LT_4_TDR_Long_All REAL,
                Concentration_Net_LT_4_TDR_Short_All REAL,
                Concentration_Net_LT_8_TDR_Long_All REAL,
                Concentration_Net_LT_8_TDR_Short_All REAL,
                Concentration_Gross_LT_4_TDR_Long_Old REAL,
                Concentration_Gross_LT_4_TDR_Short_Old REAL,
                Concentration_Gross_LT_8_TDR_Long_Old REAL,
                Concentration_Gross_LT_8_TDR_Short_Old REAL,
                Concentration_Net_LT_4_TDR_Long_Old REAL,
                Concentration_Net_LT_4_TDR_Short_Old REAL,
                Concentration_Net_LT_8_TDR_Long_Old REAL,
                Concentration_Net_LT_8_TDR_Short_Old REAL,
                Concentration_Gross_LT_4_TDR_Long_Other REAL,
                Concentration_Gross_LT_4_TDR_ShortOther REAL,
                Concentration_Gross_LT_8_TDR_Long_Other REAL,
                Concentration_Gross_LT_8_TDR_ShortOther REAL,
                Concentration_Net_LT_4_TDR_Long_Other REAL,
                Concentration_Net_LT_4_TDR_Short_Other REAL,
                Concentration_Net_LT_8_TDR_Long_Other REAL,
                Concentration_Net_LT_8_TDR_Short_Other REAL,
                Contract_Units TEXT,
                CFTC_Contract_Market_Code_Quotes REAL,
                CFTC_Market_Code_in_Initials_Quotes TEXT,
                CFTC_Commodity_Code_Quotes REAL,
                FutOnly_or_Combined TEXT,
                PRIMARY KEY (
                    Market_and_Exchange_Names,
                    Report_Date_as_YYYY_MM_DD,
                    FutOnly_or_Combined
                )
            )
        """

        self.sql_insert = """
            INSERT OR IGNORE INTO TBL_COMMITMENTSOFTRADERS_LONGFORMAT (
                Market_and_Exchange_Names,
                As_of_Date_in_Form_YYMMDD,
                Report_Date_as_YYYY_MM_DD,
                CFTC_Contract_Market_Code,
                CFTC_Market_Code_in_Initials,
                CFTC_Region_Code,
                CFTC_Commodity_Code,
                Open_Interest_All,
                Noncommercial_Positions_Long_All,
                Noncommercial_Positions_Short_All,
                Noncommercial_Positions_Spreading_All,
                Commercial_Positions_Long_All,
                Commercial_Positions_Short_All,
                Total_Reportable_Positions_Long_All,
                Total_Reportable_Positions_Short_All,
                Nonreportable_Positions_Long_All,
                Nonreportable_Positions_Short_All,
                Open_Interest_Old,
                Noncommercial_Positions_Long_Old,
                Noncommercial_Positions_Short_Old,
                Noncommercial_Positions_Spreading_Old,
                Commercial_Positions_Long_Old,
                Commercial_Positions_Short_Old,
                Total_Reportable_Positions_Long_Old,
                Total_Reportable_Positions_Short_Old,
                Nonreportable_Positions_Long_Old,
                Nonreportable_Positions_Short_Old,
                Open_Interest_Other,
                Noncommercial_Positions_Long_Other,
                Noncommercial_Positions_Short_Other,
                Noncommercial_Positions_Spreading_Other,
                Commercial_Positions_Long_Other,
                Commercial_Positions_Short_Other,
                Total_Reportable_Positions_Long_Other,
                Total_Reportable_Positions_Short_Other,
                Nonreportable_Positions_Long_Other,
                Nonreportable_Positions_Short_Other,
                Change_in_Open_Interest_All,
                Change_in_Noncommercial_Long_All,
                Change_in_Noncommercial_Short_All,
                Change_in_Noncommercial_Spreading_All,
                Change_in_Commercial_Long_All,
                Change_in_Commercial_Short_All,
                Change_in_Total_Reportable_Long_All,
                Change_in_Total_Reportable_Short_All,
                Change_in_Nonreportable_Long_All,
                Change_in_Nonreportable_Short_All,
                Pct_of_Open_Interest_OI_All,
                Pct_of_OI_Noncommercial_Long_All,
                Pct_of_OI_Noncommercial_Short_All,
                Pct_of_OI_Noncommercial_Spreading_All,
                Pct_of_OI_Commercial_Long_All,
                Pct_of_OI_Commercial_Short_All,
                Pct_of_OI_Total_Reportable_Long_All,
                Pct_of_OI_Total_Reportable_Short_All,
                Pct_of_OI_Nonreportable_Long_All,
                Pct_of_OI_Nonreportable_Short_All,
                Pct_of_Open_Interest_OIOld,
                Pct_of_OI_Noncommercial_Long_Old,
                Pct_of_OI_Noncommercial_Short_Old,
                Pct_of_OI_Noncommercial_Spreading_Old,
                Pct_of_OI_Commercial_Long_Old,
                Pct_of_OI_Commercial_Short_Old,
                Pct_of_OI_Total_Reportable_Long_Old,
                Pct_of_OI_Total_Reportable_Short_Old,
                Pct_of_OI_Nonreportable_Long_Old,
                Pct_of_OI_Nonreportable_Short_Old,
                Pct_of_Open_Interest_OI_Other,
                Pct_of_OI_Noncommercial_Long_Other,
                Pct_of_OI_Noncommercial_Short_Other,
                Pct_of_OI_Noncommercial_Spreading_Other,
                Pct_of_OI_Commercial_Long_Other,
                Pct_of_OI_Commercial_Short_Other,
                Pct_of_OI_Total_Reportable_Long_Other,
                Pct_of_OI_Total_Reportable_Short_Other,
                Pct_of_OI_Nonreportable_Long_Other,
                Pct_of_OI_Nonreportable_Short_Other,
                Traders_Total_All,
                Traders_Noncommercial_Long_All,
                Traders_Noncommercial_Short_All,
                Traders_Noncommercial_Spreading_All,
                Traders_Commercial_Long_All,
                Traders_Commercial_Short_All,
                Traders_Total_Reportable_Long_All,
                Traders_Total_Reportable_Short_All,
                Traders_Total_Old,
                Traders_Noncommercial_Long_Old,
                Traders_Noncommercial_Short_Old,
                Traders_Noncommercial_Spreading_Old,
                Traders_Commercial_Long_Old,
                Traders_Commercial_Short_Old,
                Traders_Total_Reportable_Long_Old,
                Traders_Total_Reportable_Short_Old,
                Traders_Total_Other,
                Traders_Noncommercial_Long_Other,
                Traders_Noncommercial_Short_Other,
                Traders_Noncommercial_Spreading_Other,
                Traders_Commercial_Long_Other,
                Traders_Commercial_Short_Other,
                Traders_Total_Reportable_Long_Other,
                Traders_Total_Reportable_Short_Other,
                Concentration_Gross_LT_4_TDR_Long_All,
                Concentration_Gross_LT_4_TDR_Short_All,
                Concentration_Gross_LT_8_TDR_Long_All,
                Concentration_Gross_LT_8_TDR_Short_All,
                Concentration_Net_LT_4_TDR_Long_All,
                Concentration_Net_LT_4_TDR_Short_All,
                Concentration_Net_LT_8_TDR_Long_All,
                Concentration_Net_LT_8_TDR_Short_All,
                Concentration_Gross_LT_4_TDR_Long_Old,
                Concentration_Gross_LT_4_TDR_Short_Old,
                Concentration_Gross_LT_8_TDR_Long_Old,
                Concentration_Gross_LT_8_TDR_Short_Old,
                Concentration_Net_LT_4_TDR_Long_Old,
                Concentration_Net_LT_4_TDR_Short_Old,
                Concentration_Net_LT_8_TDR_Long_Old,
                Concentration_Net_LT_8_TDR_Short_Old,
                Concentration_Gross_LT_4_TDR_Long_Other,
                Concentration_Gross_LT_4_TDR_ShortOther,
                Concentration_Gross_LT_8_TDR_Long_Other,
                Concentration_Gross_LT_8_TDR_ShortOther,
                Concentration_Net_LT_4_TDR_Long_Other,
                Concentration_Net_LT_4_TDR_Short_Other,
                Concentration_Net_LT_8_TDR_Long_Other,
                Concentration_Net_LT_8_TDR_Short_Other,
                Contract_Units,
                CFTC_Contract_Market_Code_Quotes,
                CFTC_Market_Code_in_Initials_Quotes,
                CFTC_Commodity_Code_Quotes,
                FutOnly_or_Combined
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        self.sql_merge_long_short_fmt = """
            select
              tbl_short.Market_and_Exchange_Names
              , tbl_short.Report_Date_as_YYYY_MM_DD
              , tbl_short.CFTC_Market_Code
              , tbl_short.Contract_Units
              , tbl_short.FutOnly_or_Combined
              , tbl_short.Open_Interest_All
              , Dealer_Positions_Long_All
              , Dealer_Positions_Short_All
              , Dealer_Positions_Spread_All
              , Asset_Mgr_Positions_Long_All
              , Asset_Mgr_Positions_Short_All
              , Asset_Mgr_Positions_Spread_All
              , Lev_Money_Positions_Long_All
              , Lev_Money_Positions_Short_All
              , Lev_Money_Positions_Spread_All
              , Other_Rept_Positions_Long_All
              , Other_Rept_Positions_Short_All
              , Other_Rept_Positions_Spread_All
              , Tot_Rept_Positions_Long_All
              , Tot_Rept_Positions_Short_All
              , NonRept_Positions_Long_All
              , NonRept_Positions_Short_All
              , tbl_short.Change_in_Open_Interest_All
              , Change_in_Dealer_Long_All
              , Change_in_Dealer_Short_All
              , Change_in_Dealer_Spread_All
              , Change_in_Asset_Mgr_Long_All
              , Change_in_Asset_Mgr_Short_All
              , Change_in_Asset_Mgr_Spread_All
              , Change_in_Lev_Money_Long_All
              , Change_in_Lev_Money_Short_All
              , Change_in_Lev_Money_Spread_All
              , Change_in_Other_Rept_Long_All
              , Change_in_Other_Rept_Short_All
              , Change_in_Other_Rept_Spread_All
              , Change_in_Tot_Rept_Long_All
              , Change_in_Tot_Rept_Short_All
              , Change_in_NonRept_Long_All
              , Change_in_NonRept_Short_All
              , Pct_of_Open_Interest_All
              , Pct_of_OI_Dealer_Long_All
              , Pct_of_OI_Dealer_Short_All
              , Pct_of_OI_Dealer_Spread_All
              , Pct_of_OI_Asset_Mgr_Long_All
              , Pct_of_OI_Asset_Mgr_Short_All
              , Pct_of_OI_Asset_Mgr_Spread_All
              , Pct_of_OI_Lev_Money_Long_All
              , Pct_of_OI_Lev_Money_Short_All
              , Pct_of_OI_Lev_Money_Spread_All
              , Pct_of_OI_Other_Rept_Long_All
              , Pct_of_OI_Other_Rept_Short_All
              , Pct_of_OI_Other_Rept_Spread_All
              , Pct_of_OI_Tot_Rept_Long_All
              , Pct_of_OI_Tot_Rept_Short_All
              , Pct_of_OI_NonRept_Long_All
              , Pct_of_OI_NonRept_Short_All
              , Traders_Tot_All
              , Traders_Dealer_Long_All
              , Traders_Dealer_Short_All
              , Traders_Dealer_Spread_All
              , Traders_Asset_Mgr_Long_All
              , Traders_Asset_Mgr_Short_All
              , Traders_Asset_Mgr_Spread_All
              , Traders_Lev_Money_Long_All
              , Traders_Lev_Money_Short_All
              , Traders_Lev_Money_Spread_All
              , Traders_Other_Rept_Long_All
              , Traders_Other_Rept_Short_All
              , Traders_Other_Rept_Spread_All
              , Traders_Tot_Rept_Long_All
              , Traders_Tot_Rept_Short_All
              , tbl_long.Open_Interest_All as Open_Interest_All_LongFmt
              , Noncommercial_Positions_Long_All
              , Noncommercial_Positions_Short_All
              , Noncommercial_Positions_Spreading_All
              , Commercial_Positions_Long_All
              , Commercial_Positions_Short_All
              , Total_Reportable_Positions_Long_All
              , Total_Reportable_Positions_Short_All
              , Nonreportable_Positions_Long_All
              , Nonreportable_Positions_Short_All
              , tbl_long.Change_in_Open_Interest_All AS Change_in_Open_Interest_All_LongFmt
              , Change_in_Noncommercial_Long_All
              , Change_in_Noncommercial_Short_All
              , Change_in_Noncommercial_Spreading_All
              , Change_in_Commercial_Long_All
              , Change_in_Commercial_Short_All
              , Change_in_Total_Reportable_Long_All
              , Change_in_Total_Reportable_Short_All
              , Change_in_Nonreportable_Long_All
              , Change_in_Nonreportable_Short_All
              , Pct_of_Open_Interest_OI_All
              , Pct_of_OI_Noncommercial_Long_All
              , Pct_of_OI_Noncommercial_Short_All
              , Pct_of_OI_Noncommercial_Spreading_All
              , Pct_of_OI_Commercial_Long_All
              , Pct_of_OI_Commercial_Short_All
              , Pct_of_OI_Total_Reportable_Long_All
              , Pct_of_OI_Total_Reportable_Short_All
              , Pct_of_OI_Nonreportable_Long_All
              , Pct_of_OI_Nonreportable_Short_All
              , tbl_long.Traders_Total_All as Traders_Total_All_LongFmt
              , Traders_Noncommercial_Long_All
              , Traders_Noncommercial_Short_All
              , Traders_Noncommercial_Spreading_All
              , Traders_Commercial_Long_All
              , Traders_Commercial_Short_All
              , Traders_Total_Reportable_Long_All
              , Traders_Total_Reportable_Short_All
            from
              TBL_COMMITMENTSOFTRADERS_SHORTFORMAT tbl_short
            INNER JOIN
              TBL_COMMITMENTSOFTRADERS_LONGFORMAT tbl_long
            ON
              tbl_short.Market_and_Exchange_Names = tbl_long.Market_and_Exchange_Names
              AND tbl_short.Report_Date_as_YYYY_MM_DD = tbl_long.Report_Date_as_YYYY_MM_DD
              AND tbl_short.CFTC_Market_Code = tbl_long.CFTC_Market_Code_in_Initials
              AND tbl_short.FutOnly_or_Combined = tbl_long.FutOnly_or_Combined
            order by
              tbl_short.Report_Date_as_YYYY_MM_DD desc
              , tbl_short.CFTC_Market_Code
              , tbl_short.Contract_Units
              , tbl_short.FutOnly_or_Combined
        """
        self.create_table()

    def get_summary(self, exchange_name='CME'):
        df = self.select(self.sql_merge_long_short_fmt, True, True)
        df = df[df['CFTC_Market_Code'].str.contains(exchange_name)]
        df['Report_Date_as_YYYY_MM_DD'] = pd.to_datetime(df['Report_Date_as_YYYY_MM_DD'])
        df_summ = df.pivot_table(
            index=['Report_Date_as_YYYY_MM_DD'],
            columns=['FutOnly_or_Combined', 'Market_and_Exchange_Names'],
            values=[
                'Lev_Money_Positions_Long_All',
                'Lev_Money_Positions_Short_All',
                'Tot_Rept_Positions_Long_All',
                'Tot_Rept_Positions_Short_All',
                'NonRept_Positions_Long_All',
                'NonRept_Positions_Short_All'
            ],
            fill_value=0,
            aggfunc='sum'
        )
        df_summ = df_summ.asfreq('1D', method='ffill')

        df_summ[('Lev_Long_OI', 'FutOnly', 'BTC+uBTC')] = 5*df_summ[('Lev_Money_Positions_Long_All', 'FutOnly', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] + 0.1*df_summ[('Lev_Money_Positions_Long_All', 'FutOnly', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_Short_OI', 'FutOnly', 'BTC+uBTC')] = -5*df_summ[('Lev_Money_Positions_Short_All', 'FutOnly', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] - 0.1*df_summ[('Lev_Money_Positions_Short_All', 'FutOnly', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_OI', 'FutOnly', 'BTC+uBTC')] = df_summ[('Lev_Long_OI', 'FutOnly', 'BTC+uBTC')] + df_summ[('Lev_Short_OI', 'FutOnly', 'BTC+uBTC')]

        df_summ[('Lev_Long_OI', 'FutOnly', 'ETH')] = 5*df_summ[('Lev_Money_Positions_Long_All', 'FutOnly', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_Short_OI', 'FutOnly', 'ETH')] = -5*df_summ[('Lev_Money_Positions_Short_All', 'FutOnly', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_OI', 'FutOnly', 'ETH')]  = df_summ[('Lev_Long_OI', 'FutOnly', 'ETH')] + df_summ[('Lev_Short_OI', 'FutOnly', 'ETH')]

        df_summ[('All_Long_OI', 'FutOnly', 'BTC+uBTC')] = 5*df_summ[('Tot_Rept_Positions_Long_All', 'FutOnly', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] + 0.1*df_summ[('Tot_Rept_Positions_Long_All', 'FutOnly', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_Short_OI', 'FutOnly', 'BTC+uBTC')] = -5*df_summ[('Tot_Rept_Positions_Short_All', 'FutOnly', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] - 0.1*df_summ[('Tot_Rept_Positions_Short_All', 'FutOnly', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_OI', 'FutOnly', 'BTC+uBTC')] = df_summ[('All_Long_OI', 'FutOnly', 'BTC+uBTC')]  + df_summ[('All_Short_OI', 'FutOnly', 'BTC+uBTC')]

        df_summ[('All_Long_OI', 'FutOnly', 'ETH')] = 5*df_summ[('Tot_Rept_Positions_Long_All', 'FutOnly', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_Short_OI', 'FutOnly', 'ETH')] = -5*df_summ[('Tot_Rept_Positions_Short_All', 'FutOnly', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_OI', 'FutOnly', 'ETH')] = df_summ[('All_Long_OI', 'FutOnly', 'ETH')] + df_summ[('All_Short_OI', 'FutOnly', 'ETH')]

        df_summ[('Lev_Long_Ratio', 'FutOnly', 'BTC+uBTC')] = df_summ[('Lev_Long_OI', 'FutOnly', 'BTC+uBTC')] / (df_summ[('Lev_Long_OI', 'FutOnly', 'BTC+uBTC')] - df_summ[('Lev_Short_OI', 'FutOnly', 'BTC+uBTC')])
        df_summ[('Lev_Short_Ratio', 'FutOnly', 'BTC+uBTC')] = -df_summ[('Lev_Short_OI', 'FutOnly', 'BTC+uBTC')] / (df_summ[('Lev_Long_OI', 'FutOnly', 'BTC+uBTC')] - df_summ[('Lev_Short_OI', 'FutOnly', 'BTC+uBTC')])

        df_summ[('All_Long_Ratio', 'FutOnly', 'BTC+uBTC')] = df_summ[('All_Long_OI', 'FutOnly', 'BTC+uBTC')] / (df_summ[('All_Long_OI', 'FutOnly', 'BTC+uBTC')] - df_summ[('All_Short_OI', 'FutOnly', 'BTC+uBTC')])
        df_summ[('All_Short_Ratio', 'FutOnly', 'BTC+uBTC')] = -df_summ[('All_Short_OI', 'FutOnly', 'BTC+uBTC')] / (df_summ[('All_Long_OI', 'FutOnly', 'BTC+uBTC')] - df_summ[('All_Short_OI', 'FutOnly', 'BTC+uBTC')])

        df_summ[('Lev_Long_OI', 'Combined', 'BTC+uBTC')] = 5*df_summ[('Lev_Money_Positions_Long_All', 'Combined', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] + 0.1*df_summ[('Lev_Money_Positions_Long_All', 'Combined', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_Short_OI', 'Combined', 'BTC+uBTC')] = -5*df_summ[('Lev_Money_Positions_Short_All', 'Combined', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] - 0.1*df_summ[('Lev_Money_Positions_Short_All', 'Combined', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_OI', 'Combined', 'BTC+uBTC')] = df_summ[('Lev_Long_OI', 'Combined', 'BTC+uBTC')] + df_summ[('Lev_Short_OI', 'Combined', 'BTC+uBTC')]

        df_summ[('Lev_Long_OI', 'Combined', 'ETH')] = 5*df_summ[('Lev_Money_Positions_Long_All', 'Combined', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_Short_OI', 'Combined', 'ETH')] = -5*df_summ[('Lev_Money_Positions_Short_All', 'Combined', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('Lev_OI', 'Combined', 'ETH')] = df_summ[('Lev_Long_OI', 'Combined', 'ETH')] + df_summ[('Lev_Short_OI', 'Combined', 'ETH')]

        df_summ[('All_Long_OI', 'Combined', 'BTC+uBTC')] = 5*df_summ[('Tot_Rept_Positions_Long_All', 'Combined', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] + 0.1*df_summ[('Tot_Rept_Positions_Long_All', 'Combined', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_Short_OI', 'Combined', 'BTC+uBTC')] = -5*df_summ[('Tot_Rept_Positions_Short_All', 'Combined', 'BITCOIN - CHICAGO MERCANTILE EXCHANGE')] - 0.1*df_summ[('Tot_Rept_Positions_Short_All', 'Combined', 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_OI', 'Combined', 'BTC+uBTC')] = df_summ[('All_Long_OI', 'Combined', 'BTC+uBTC')] + df_summ[('All_Short_OI', 'Combined', 'BTC+uBTC')]

        df_summ[('All_Long_OI', 'Combined', 'ETH')] = 5*df_summ[('Tot_Rept_Positions_Long_All', 'Combined', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_Short_OI', 'Combined', 'ETH')] = -5*df_summ[('Tot_Rept_Positions_Short_All', 'Combined', 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE')]
        df_summ[('All_OI', 'Combined', 'ETH')] = df_summ[('All_Long_OI', 'Combined', 'ETH')] + df_summ[('All_Short_OI', 'Combined', 'ETH')]

        df_summ[('Lev_Long_Ratio', 'Combined', 'BTC+uBTC')] = df_summ[('Lev_Long_OI', 'Combined', 'BTC+uBTC')] / (df_summ[('Lev_Long_OI', 'Combined', 'BTC+uBTC')] - df_summ[('Lev_Short_OI', 'Combined', 'BTC+uBTC')])
        df_summ[('Lev_Short_Ratio', 'Combined', 'BTC+uBTC')] = -df_summ[('Lev_Short_OI', 'Combined', 'BTC+uBTC')] / (df_summ[('Lev_Long_OI', 'Combined', 'BTC+uBTC')] - df_summ[('Lev_Short_OI', 'Combined', 'BTC+uBTC')])

        df_summ[('All_Long_Ratio', 'Combined', 'BTC+uBTC')] = df_summ[('All_Long_OI', 'Combined', 'BTC+uBTC')] / (df_summ[('All_Long_OI', 'Combined', 'BTC+uBTC')] - df_summ[('All_Short_OI', 'Combined', 'BTC+uBTC')])
        df_summ[('All_Short_Ratio', 'Combined', 'BTC+uBTC')] = -df_summ[('All_Short_OI', 'Combined', 'BTC+uBTC')] / (df_summ[('All_Long_OI', 'Combined', 'BTC+uBTC')] - df_summ[('All_Short_OI', 'Combined', 'BTC+uBTC')])

        # df_summ = df_summ.merge(df_price, left_index=True, right_index=True)
        df_summ2 = df_summ[[
            ('Lev_Long_Ratio', 'FutOnly', 'BTC+uBTC'),
            ('Lev_Short_Ratio', 'FutOnly', 'BTC+uBTC'),
            ('Lev_Long_OI', 'FutOnly', 'BTC+uBTC'),
            ('Lev_Short_OI', 'FutOnly', 'BTC+uBTC'),
            ('Lev_OI', 'FutOnly', 'BTC+uBTC'),
            ('Lev_Long_OI', 'FutOnly', 'ETH'),
            ('Lev_Short_OI', 'FutOnly', 'ETH'),
            ('Lev_OI', 'FutOnly', 'ETH'),

            ('All_Long_Ratio', 'FutOnly', 'BTC+uBTC'),
            ('All_Short_Ratio', 'FutOnly', 'BTC+uBTC'),
            ('All_Long_OI', 'FutOnly', 'BTC+uBTC'),
            ('All_Short_OI', 'FutOnly', 'BTC+uBTC'),
            ('All_OI', 'FutOnly', 'BTC+uBTC'),
            ('All_Long_OI', 'FutOnly', 'ETH'),
            ('All_Short_OI', 'FutOnly', 'ETH'),
            ('All_OI', 'FutOnly', 'ETH'),

            ('Lev_Long_Ratio', 'Combined', 'BTC+uBTC'),
            ('Lev_Short_Ratio', 'Combined', 'BTC+uBTC'),
            ('Lev_Long_OI', 'Combined', 'BTC+uBTC'),
            ('Lev_Short_OI', 'Combined', 'BTC+uBTC'),
            ('Lev_OI', 'Combined', 'BTC+uBTC'),
            ('Lev_Long_OI', 'Combined', 'ETH'),
            ('Lev_Short_OI', 'Combined', 'ETH'),
            ('Lev_OI', 'Combined', 'ETH'),

            ('All_Long_Ratio', 'Combined', 'BTC+uBTC'),
            ('All_Short_Ratio', 'Combined', 'BTC+uBTC'),
            ('All_Long_OI', 'Combined', 'BTC+uBTC'),
            ('All_Short_OI', 'Combined', 'BTC+uBTC'),
            ('All_OI', 'Combined', 'BTC+uBTC'),
            ('All_Long_OI', 'Combined', 'ETH'),
            ('All_Short_OI', 'Combined', 'ETH'),
            ('All_OI', 'Combined', 'ETH')
            #('BTC', 'BTC', 'BTC'),
            #('log_BTC', 'log_BTC', 'log_BTC'),
            #('ETH', 'ETH', 'ETH'),
            #('log_ETH', 'log_ETH', 'log_ETH')
        ]]

        return df_summ2