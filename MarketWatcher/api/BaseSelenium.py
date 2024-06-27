# -*- coding, utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from logging import getLogger
logger = getLogger(__name__)

class BaseSelenium():
    def __init__(self):
        try:
            self.WAIT_SECOND_INITIAL = 6
            self.WAIT_SECOND_CLICK = 1.5
            # self.WAIT_NORMAL = 2
            self.WAIT_NORMAL = 10
            self.visible = True
            self.driver_option = webdriver.ChromeOptions()
            if not self.visible:
                self.driver_option.add_argument('--headless')
            self.driver_option.add_argument('--disable-gpu')
            self.driver_option.add_argument('--window-size=1800x1200')
            self.user_agent_str = r'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            self.driver_option.add_argument(self.user_agent_str)
           
            # self.driver_name = 'chromedriver.exe'
            # self.driver_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.driver_name))
            # self.driver = webdriver.Chrome(self.driver_path, options=self.driver_option)
           
            # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.driver_option)
            
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.driver_option)
            # self.driver.get('https://google.com')

        except Exception as e:
            logger.error(e.args)

    def __del__(self):
        self.driver.quit()

    def quit_browser(self):
        self.driver.quit()

    def navigate(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(self.WAIT_SECOND_INITIAL)

    def wait_expected_condition(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located)
        # self.driver.implicitly_wait(self.WAIT_SECOND_CLICK)
        time.sleep(self.WAIT_NORMAL)