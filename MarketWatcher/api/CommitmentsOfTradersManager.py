# -*- coding,  utf-8 -*-

import datetime
import pandas as pd
import os
import urllib
import ssl
from util.string_util import safe_float
from database.CommitmentsOfTradersShortFormatTableManager import CommitmentsOfTradersShortFormatTableManager
from database.CommitmentsOfTradersLongFormatTableManager import CommitmentsOfTradersLongFormatTableManager

from logging import getLogger
logger = getLogger(__name__)

class CommitmentOfTradersManager:
    def __init__(self):
        self.url_cftc_short_format = {
            'FutOnly': 'https://www.cftc.gov/files/dea/history/fut_fin_txt_{}.zip',
            'Combined': 'https://www.cftc.gov/files/dea/history/com_fin_txt_{}.zip'
        }

        self.url_cftc_long_format = {
            'FutOnly': 'https://www.cftc.gov/files/dea/history/deacot{}.zip',
            'Combined': 'https://www.cftc.gov/files/dea/history/deahistfo{}.zip'
        }

    @staticmethod
    def format_columns(df):
        if 'As of Date in Form YYYY-MM-DD' in df.columns:
            df = df.rename(columns={'As of Date in Form YYYY-MM-DD': 'Report_Date_as_YYYY_MM_DD'})

        for col in df.columns:
            new_col = col
            new_col = new_col.replace(' ', '_')
            new_col = new_col.replace('-', '_')
            new_col = new_col.replace('-', '_')
            new_col = new_col.replace('%', 'Pct')
            new_col = new_col.replace('(', '')
            new_col = new_col.replace(')', '')
            new_col = new_col.replace('=_', '')
            new_col = new_col.replace('=', '')
            new_col = new_col.replace(
                '_Total_Reportable_Positions_Long_All', 'Total_Reportable_Positions_Long_All')
            df = df.rename(columns={col: new_col})
        return df

    @staticmethod
    def read_csv(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.90 '
                          'Safari/537.36'
        }
        request = urllib.request.Request(url=url, headers=headers)
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'output', os.path.split(url)[-1])
        context = ssl._create_unverified_context()
        with open(file_name, "wb") as f:
            f.write(urllib.request.urlopen(request, context=context).read())
        df = pd.read_csv(file_name)
        return df

    def download_all_zip(self, is_short_format=True):
        from_year = datetime.date.today().year
        end_year = datetime.date.today().year + 1
        df = None
        urls = self.url_cftc_short_format if is_short_format else self.url_cftc_long_format
        for k, v in urls.items():
            for y in range(from_year, end_year):
                urltmp = v.format(y)
                # tmpdf = pd.read_csv(urltmp)
                tmpdf = self.read_csv(urltmp)
                if not 'FutOnly_or_Combined' in tmpdf.columns:
                    tmpdf['FutOnly_or_Combined'] = k
                df = tmpdf if df is None else pd.concat([df, tmpdf], ignore_index=True)
        return df

    def convert_dtypes(self, df):
        for col in df.columns:
            if 'All' in col:
                df[col] = df[col].map(safe_float)
                df.astype({col: 'float'})
        return df

    def get_commitments_of_traders(self, is_short_format=True):
        df = self.download_all_zip(is_short_format)
        df = self.format_columns(df)
        df = df[df['Market_and_Exchange_Names'].str.contains('BITCOIN|ETHER')]
        sort_values = [
            'FutOnly_or_Combined',
            'Market_and_Exchange_Names',
            'Report_Date_as_YYYY_MM_DD'
        ]
        df = df.sort_values(sort_values)
        df = self.convert_dtypes(df)
        df = df.reset_index(drop=True)
        return df

    def update_db(self, is_short_format=True):
        try:
            db = CommitmentsOfTradersShortFormatTableManager() if is_short_format else CommitmentsOfTradersLongFormatTableManager()
            df = self.get_commitments_of_traders(is_short_format)
            logger.info('commitments of traders files have been downloaded.')
            db.insert_many(df.values)
            logger.info('[{} inserted] DB execution completed.'.format(len(df)))
        except Exception as e:
            logger.error('Updating commitments of traders failed.')
            logger.error(e.args)

    def update_db_all(self):
        self.update_db(True)
        self.update_db(False)
