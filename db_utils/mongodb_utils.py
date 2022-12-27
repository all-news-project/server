import os
from typing import List

from pymongo import MongoClient

from db_utils.exceptions import DataNotFoundException, InsertDataException
from kg_logger import KGLogger, log_function


class MongoDBUtils:
    DB_NAME = os.getenv(key='DB_NAME', default='local_restore')
    DB_PASSWORD = os.getenv(key='DB_PASSWORD')
    DB_URL = os.getenv(key='DB_URL')

    def __init__(self):
        self.logger = KGLogger()
        client = MongoClient(f'mongodb+srv://allnews:{self.DB_PASSWORD}@{self.DB_URL}')
        self._db = client[self.DB_NAME]
        self.logger.debug(f"Connected to mongodb ")

    @log_function
    def insert_one(self, table_name: str, data: dict):
        try:
            self.logger.debug(f"Trying to insert data to table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].insert_one(data)
            if res:
                self.logger.info(f"Successfully inserted data to db, object id: {str(res.inserted_id)}")
            else:
                desc = f"Error insert data: {data}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise InsertDataException(desc)
        except Exception as e:
            self.logger.error(f"Error insert data to db - {str(e)}")
            raise e

    @log_function
    def insert_many(self, table_name: str, data_list: List[dict]):
        if not data_list:
            self.logger.warning(f"Error insert many to db, data list is empty")
            return
        try:
            self.logger.debug(f"Trying to insert {len(data_list)} to table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].insert_many(data_list)
            if res:
                for inserted_id in res.inserted_ids:
                    self.logger.info(f"Successfully inserted data to db, object id: {str(inserted_id)}")
            else:
                desc = f"Error insert data: {data_list}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise InsertDataException(desc)
        except Exception as e:
            self.logger.error(f"Error insert data to db - {str(e)}")
            raise e

    @log_function
    def get_one(self, table_name: str, data_filter: dict) -> dict:
        try:
            self.logger.debug(f"Trying to get one data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].find_one(data_filter)
            if res:
                object_id = res.get('_id')
                self.logger.info(f"Got data from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return dict(res)
            else:
                desc = f"Error find data with filter: {data_filter}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise DataNotFoundException(desc)
        except Exception as e:
            self.logger.error(f"Error get one from db - {str(e)}")
            raise e

    # TODO: add method get_many by table_name: str and data_filter: dict
    # TODO: add method delete_one by table_name: str and data_filter: dict
    # TODO: add method delete_many by table_name: str and data_filter: dict
    # TODO: add method update_one by table_name: str and data_fileter: dict and new_data: dict
    # TODO: add method update_many by table_name: str and data_fileter: dict and new_data: dict
    # TODO: add method count by table_name: str, and data_filter: dict -> int
    # TODO: add method exists by table name: str and data_filter: dict -> bool
