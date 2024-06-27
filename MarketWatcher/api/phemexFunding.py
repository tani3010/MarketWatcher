
# -*- coding: utf-8 -*-

import pandas as pd
import pytz
import dateutil
from time import time
from datetime import datetime, timezone, timedelta
from database.FundingRateTableManager import FundingRateTableManager
from selenium.webdriver.common.by import By
import os
import yaml

from .BaseSelenium import BaseSelenium

from logging import getLogger
logger = getLogger(__name__)

class Phemex(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.URL_BASE = r'https://phemex.com/ja/contract/funding-history'
        self.yaml_file_name = 'config.yml'
        self.yaml_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'config', self.yaml_file_name))
        with open(self.yaml_path) as file:
            self.yaml = yaml.safe_load(file)

    def update_phemex_fundingRate(self):
        db = FundingRateTableManager()
        result_dict = {}
        df_daily_phemex = pd.DataFrame()

        self.navigate(self.URL_BASE)

        # tmp = self.driver.find_elements_by_xpath("//li[@class='pr T2 cp ph10 svelte-r327t8']")
        tmp = self.driver.find_element(By.XPATH, "//li[@class='pr T2 cp ph10 svelte-r327t8']")

        product_count = len(tmp)
        product_list = self.yaml['ExchangeSetting']['phemex']['products']
        for i in range(2, product_count+2):

            self.navigate(self.URL_BASE)
            self.wait_expected_condition()

            # xpath = r'/html/body/div[1]/div[2]/div/div/div/div[1]/div/div[2]'
            xpath = r'/html/body/div[1]/div[3]/div/div/div/div[1]/div/div[2]'

            # btn = self.driver.find_element_by_xpath(xpath)
            btn = self.driver.find_element(By.XPATH, xpath)
            
            btn.click()
            self.wait_expected_condition()
            
            # xpath = r'/html/body/div[1]/div[2]/div/div/div/div[1]/div/div[2]/ul/li[{}]'.format(i)
            xpath = r'/html/body/div[1]/div[3]/div/div/div/div[1]/div/div[2]/ul/li[{}]'.format(i)

            # btn = self.driver.find_element_by_xpath(xpath)
            btn = self.driver.find_element(By.XPATH, xpath)

            product_name = btn.text.replace('\n', ' ')

            if len(product_list) == 0:
                break
            
            if not product_name in product_list:
                continue

            btn.click()
            self.wait_expected_condition()

            next_btn = None
            count = 0
            try:
                product_list.remove(product_name)
                while True:
                    # fr_web_list = self.driver.find_elements_by_css_selector(".td.T2.svelte-15wjsvk")
                    # fr_web_list = self.driver.find_elements_by_css_selector(".td.T2.svelte-o5ul1o")
                    fr_web_list = self.driver.find_elements(By.CSS_SELECTOR, ".td.T2.svelte-o5ul1o")
                    for j in range(0, len(fr_web_list), 4):
                        timestamp = fr_web_list[j].text
                        product_code = fr_web_list[j+1].text
                        fr = float((fr_web_list[j+3].text).replace("%","").replace('0.', '0.00'))

                        if timestamp != '1969-12-31 19:00:00':
                            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                            dt = dt.replace(tzinfo=dateutil.tz.tzlocal())
                            dt = dt.astimezone(tz=timezone.utc)

                            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')

                            tmp_dict = {
                                'timestamp': dt.timestamp(),
                                'datetime': timestamp,
                                'product_code': product_code,
                                'fundingRate': fr
                            }
                            df_daily_phemex = pd.concat([df_daily_phemex, pd.DataFrame(tmp_dict, index=[0])], ignore_index=True)

                    try:
                        if next_btn is None:
                            # next_btn = self.driver.find_element_by_css_selector(".next.svelte-3tqfek")
                            next_btn = self.driver.find_element(By.CSS_SELECTOR, ".next.svelte-3tqfek")
                            
                        self.driver.execute_script('arguments[0].click();', next_btn)
                        self.wait_expected_condition()
                        count += 1
                        if count > 10:
                            logger.info('[{}][{} pages were loaded][{}] completed.'.format(product_code, count, self.URL_BASE))
                            break
                    except:
                        logger.info('[{}][{} pages were loaded][{}] completed.'.format(product_code, count, self.URL_BASE))
                        break

            except Exception as e:
                logger.error('unexpected error happend in {}'.format(product_name))
                logger.error(e.args)
            finally:
                if df_daily_phemex is not None and len(df_daily_phemex) > 0:
                    df_daily_phemex['exchange'] = 'phemex'
                    df_daily_phemex['updatetime'] = time()
                    df_daily_phemex = df_daily_phemex[(df_daily_phemex.fundingRate > -0.005) & (df_daily_phemex.fundingRate < 0.005)]
                    db.insert_many(
                        df_daily_phemex[['timestamp', 'updatetime', 'datetime', 'exchange', 'product_code', 'fundingRate']].values)
                    logger.info('[{} records inserted in {}] DB execution completed.'.format(len(df_daily_phemex), product_name))
                    df_daily_phemex = None

        self.quit_browser()

    def update_db(self):
        try:
            self.update_phemex_fundingRate()
        except Exception as e:
            logger.error(e.args)