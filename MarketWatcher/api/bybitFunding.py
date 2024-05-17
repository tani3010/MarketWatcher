# -*- coding: utf-8 -*-

import pandas as pd
import os
import yaml

from datetime import datetime
from time import time
from database.FundingRateTableManager import FundingRateTableManager, FundingRateMonthlyTableManager, FundingRateYearlyTableManager

from .BaseSelenium import BaseSelenium

from logging import getLogger
logger = getLogger(__name__)

class ByBit(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.yaml_file_name = 'config.yml'
        self.yaml_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'config', self.yaml_file_name))
        with open(self.yaml_path) as file:
            self.yaml = yaml.safe_load(file)

        self.TARGET_SYMBOLS = [
            self.yaml['ExchangeSetting']['bybit2']['products'],
            self.yaml['ExchangeSetting']['bybit']['products']
        ]


        self.URL_BASE = [
            'https://www.bybit.com/data/basic/linear/funding-history?symbol=',
            'https://www.bybit.com/data/basic/inverse/funding-history?symbol='
        ]

    def click_next(self, iURL):
        if iURL == 0:
            xpath = '//*[@id="root"]/div/main/section/div/div[2]/div[3]/div/div/span[2]'
        else:
            xpath = '//*[@id="root"]/div/div[2]/main/section/div/div/div[3]/div/div/span[2]'
        btn = self.driver.find_element_by_xpath(xpath)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        btn.click()
        self.driver.implicitly_wait(self.WAIT_SECOND_CLICK)

    def has_next_page(self, iURL):
        if iURL == 0:
            xpath = '//*[@id="root"]/div/main/section/div/div[2]/div[3]/div/div/span[2]'
        else:
            xpath = '//*[@id="root"]/div/div[2]/main/section/div/div/div[3]/div/div/span[2]'
        return self.driver.find_element_by_xpath(xpath).get_attribute('class') != 'disable'

    def get_current_table(self):
        df = pd.read_html(self.driver.page_source, encoding='cp932')[0]
        colname_dict = {
            'Time (UTC)': 'timestamp',
            'Funding Interval': 'fundingInterval',
            'Funding Rate': 'fundingRate'
        }

        df = df.rename(columns=colname_dict)
        df['fundingRate'] = df['fundingRate'].str.rstrip('%').astype('float')*0.01
        df['datetime'] = df['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        df = df[df.datetime > '2010-01-01']
        df = df.reset_index()
        df['timestamp'] = df['datetime'].map(lambda x: x.timestamp())
        return df

    def update_bybit_fundingRate(self):
        db = FundingRateTableManager()
        result_dict = {}
        df_daily_bybit = pd.DataFrame()

        try:
            for iURL in range(len(self.URL_BASE)):
                for symbol in self.TARGET_SYMBOLS[iURL]:
                    count = 0
                    url = self.URL_BASE[iURL] + symbol
                    self.navigate(url)
                    self.wait_expected_condition()
                    df = pd.DataFrame()
                    has_next = True
                    while has_next:
                        df_tmp = self.get_current_table()
                        df_tmp['symbol'] = symbol
                        df = pd.concat([df, df_tmp], ignore_index=True)  
                        has_next = self.has_next_page(iURL)
                        if count > 8:
                            break
                        if has_next:
                            self.click_next(iURL)
                            self.wait_expected_condition()
                            count += 1
                    df = df.drop_duplicates()
                    df['exchange'] = 'bybit'
                    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    df['updatetime'] = time()
                    df_daily_bybit = pd.concat([df_daily_bybit, df], sort=True)
                    result_dict[symbol] = df
                    logger.info('[{}][{}] completed.'.format(symbol, url))

        except Exception as e:
            logger.error('[{}]Error happend in {}.'.format(url, symbol))
            logger.error(e.args)

        finally:
            self.quit_browser()
            if len(df_daily_bybit) > 0:
                db.insert_many(
                    df_daily_bybit[['timestamp', 'updatetime', 'datetime', 'exchange', 'symbol', 'fundingRate']].values)
                logger.info('[{} records inserted] DB execution completed.'.format(len(df_daily_bybit)))

    def update_db(self):
        try:
            self.update_bybit_fundingRate()
        except Exception as e:
            logger.error(e.args)