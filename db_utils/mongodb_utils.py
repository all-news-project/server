import os
from typing import List

from bson import ObjectId
from pymongo import MongoClient

from db_utils.exceptions import DataNotFoundDBException, InsertDataDBException, DeleteDataDBException
from db_utils.interface_db_utils import DBUtilsInterface
from kg_logger import KGLogger, log_function


class DBUtils(DBUtilsInterface):
    DB_NAME = os.getenv(key='DB_NAME', default='local_restore')
    DB_PASSWORD = os.getenv(key='DB_PASSWORD')
    DB_URL = os.getenv(key='DB_URL')

    def __init__(self):
        self.logger = KGLogger()
        client = MongoClient(f'mongodb+srv://allnews:{self.DB_PASSWORD}@{self.DB_URL}')
        self._db = client[self.DB_NAME]
        self.logger.debug(f"Connected to mongodb ")

    @log_function
    def insert_one(self, table_name: str, data: dict) -> ObjectId:
        try:
            self.logger.debug(f"Trying to insert data to table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].insert_one(data)
            if res:
                self.logger.info(f"Successfully inserted data to db, object id: '{str(res.inserted_id)}'")
                return res.inserted_id
            else:
                desc = f"Error insert data: {data}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise InsertDataDBException(desc)
        except Exception as e:
            self.logger.error(f"Error insert data to db - {str(e)}")
            raise e

    @log_function
    def insert_many(self, table_name: str, data_list: List[dict]) -> List[ObjectId]:
        if not data_list:
            self.logger.warning(f"Error insert many to db, data list is empty")
            return list()
        try:
            self.logger.debug(f"Trying to insert {len(data_list)} to table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].insert_many(data_list)
            if res:
                for inserted_id in res.inserted_ids:
                    self.logger.info(f"Successfully inserted data to db, object id: {str(inserted_id)}")
                return res.inserted_ids
            else:
                desc = f"Error insert data: {data_list}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise InsertDataDBException(desc)
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
                raise DataNotFoundDBException(desc)
        except Exception as e:
            self.logger.error(f"Error get one from db - {str(e)}")
            raise e

    @log_function
    def delete_one(self, table_name: str, data_filter: dict):  # TODO: check
        try:
            self.logger.debug(f"Trying to delete onde data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self._db[table_name].delete_one(data_filter)
            if res:
                object_id = res.raw_result.get('_id')
                self.logger.info(
                    f"Deleted data from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return True
            else:
                desc = f"Error delete data with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.error(desc)
                raise DeleteDataDBException(desc)
        except Exception as e:
            self.logger.error(f"Error delete one from db: {str(e)}")
            return False

    @log_function
    def delete_many(self, table_name: str, data_filter: dict):
        pass

    @log_function
    def update_one(self, table_name: str, data_filter: dict, new_data: dict) -> ObjectId:
        pass

    @log_function
    def update_many(self, table_name: str, data_filter: dict, new_data: dict) -> List[ObjectId]:
        pass

    @log_function
    def count(self, table_name: str, data_filter: dict) -> int:
        pass

    @log_function
    def exists(self, table_name: str, data_filter: dict) -> bool:
        pass

    @log_function
    def get_many(self, table_name: str, data_filter: dict) -> List[dict]:
        pass
