# -*- coding,  utf-8 -*-

import sqlite3
import time
import os
import pandas as pd

from logging import getLogger
logger = getLogger(__name__)

class BaseDataBaseTableManager():
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.db_file_name)
        self.con = None
        self.sql_create_table = None
        self.sql_insert = None
        self.sql_upsert = None
        self.sql_vacuum = 'VACUUM'

    @staticmethod
    def get_current_time():
        return time.time()

    def execute(self, sql, insert_data=None, execute_many=False,
                with_commit=False):
        try:
            self.con = sqlite3.connect(self.db_name)
            cursor = self.con.cursor()
            if execute_many:
                if insert_data is None:
                    cursor.executemany(sql)
                else:
                    cursor.executemany(sql, insert_data)
            else:
                if insert_data is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, insert_data)

            if with_commit:
                self.con.commit()

            logger.info('DB execution completed.')
        except Exception as e:
            logger.error(e.args)
        finally:
            self.con.close()
            self.con = None

    def vacuum(self):
        self.execute(self.sql_vacuum, with_commit=True)

    def create_table(self):
        logger.info('DB execution for table creation started.')
        self.execute(self.sql_create_table, with_commit=True)

    def insert(self, insert_data):
        self.execute(self.sql_insert,
                     insert_data=insert_data, with_commit=True)

    def insert_many(self, insert_data):
        self.execute(self.sql_insert, execute_many=True,
                     insert_data=insert_data, with_commit=True)

    def upsert_many(self, insert_data):
        if self.sql_upsert is None:
            self.insert_many(insert_data)
        else:
            self.execute(self.sql_upsert, execute_many=True,
                         insert_data=insert_data, with_commit=True)

    def select(self, sql, hasHeader=False, as_df=False):
        try:
            self.con = sqlite3.connect(self.db_name)
            cursor = self.con.cursor()
            cursor.execute(sql)
            dat = cursor.fetchall()
            if hasHeader:
                header = []
                for i in cursor.description:
                    header.append(i[0])
                dat.insert(0, tuple(header))
            if as_df:
                if hasHeader:
                    dat = pd.DataFrame(dat[1:], columns=dat[0])
                else:
                    dat = pd.DataFrame(dat)
        except Exception as e:
            logger.error(e.args)
        finally:
            self.con.close()
            self.con = None
            return dat

    def fetch_all(self, table_name, hasHeader=False, as_df=False):
        sql = 'select * from {}'.format(table_name)
        dat = self.select(sql, hasHeader, as_df)
        return dat

    @staticmethod
    def set_datetime_as_index(df):
        if df.index.name == 'datetime':
            return df
        
        if 'datetime' not in df.columns:
            return df

        df.index = pd.to_datetime(df['datetime'])
        df = df.drop(columns='datetime')
        return df
