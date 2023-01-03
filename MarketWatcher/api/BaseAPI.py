# -*- coding, utf-8 -*-
import pandas as pd
import requests
from datetime import datetime

from logging import getLogger
logger = getLogger(__name__)

class BaseAPI():
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.success_code = ['<Response [200]>']
        self.error_code = ['<Response [404]>']

    def request(self, url, key=None):
        try:
            result = requests.get(url)
            if result in self.error_code:
                return None
            elif key is None:
                return result.json()
            else:
                return result.json()[key]
        except Exception as e:
            logger.error(e)
            return None

    def request_suburl(self, suburl, key=None):
        url = self.base_url + suburl
        return self.request(url, key)

    def request_dataframe(self, url, key=None):
        dat = self.request(url, key)
        return pd.DataFrame(dat)

    def request_suburl_dataframe(self, suburl, key=None):
        dat = self.request_suburl(suburl, key)
        return pd.DataFrame(dat)

    @staticmethod
    def json_to_dataframe(json):
        return pd.DataFrame(json)
