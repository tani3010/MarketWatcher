# -*- coding: utf-8 -*-
import os
import yaml

from .BaseAPI import BaseAPI
from datetime import datetime
from time import time

class APIManager(BaseAPI):
    def __init__(self):
        super().__init__()
        self.yaml_file_name = 'config.yml'
        self.yaml_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'config', self.yaml_file_name))
        self.yaml = None

    def update_db(self):
        pass

    def load_yaml(self):
        with open(self.yaml_path) as file:
            self.yaml = yaml.safe_load(file)

    @staticmethod
    def unixtime_to_datetime(unixtime):
        tmp = str(unixtime)[0:10]
        return datetime.fromtimestamp(int(tmp))

    @staticmethod
    def get_current_time():
        return time.time()

    @staticmethod
    def convert_dtypes(df, dtypes):
        for k, v in dtypes.items():
            if k in df.columns:
                df = df.astype({k: v})
        return df

    @staticmethod
    def add_column(df, col_name, value):
        if col_name not in df.columns:
            df[col_name] = value
        return df

    def add_timestamp_datetime(self, df):
        if 'datetime' in df.columns:
            tmp = df['datetime'].map(lambda x: x.upper().replace('Z', ''))
            tmp = tmp.map(lambda x: x[0:19])
            df['datetime'] = tmp.map(lambda x: datetime.fromisoformat(x).strftime('%Y-%m-%d %H:%M:%S'))
            if 'timestamp' not in df.columns:
                tmp = tmp.map(lambda x: datetime.fromisoformat(x))
                df['timestamp'] = tmp.map(lambda x: x.timestamp())
            return df

        if 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].map(lambda x: float(str(x)[0:10]))
            df['datetime'] = df['timestamp'].map(lambda x: self.unixtime_to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'))
            return df

    def add_updatetime(self, df):
        df['updatetime'] = time()
        return df
