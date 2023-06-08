import os
from typing import List

from bson import ObjectId
from pymongo import MongoClient

from db_driver.insterfaces.interface_db_driver import DBDriverInterface
from db_driver.utils.exceptions import InsertDataDBException, DataNotFoundDBException, DeleteDataDBException, \
    UpdateDataDBException
from logger import get_current_logger, log_function
from server_utils.db_utils.validation_utils import get_mongodb_connection_string


class MongoDBDriver(DBDriverInterface):
    DB_NAME = os.getenv(key='DB_NAME', default='local_restore')

    def __init__(self):
        self.logger = get_current_logger()
        self._connection_string = get_mongodb_connection_string()
        self.__client = MongoClient(self._connection_string)
        self.__db = self.__client[self.DB_NAME]
        self.logger.debug(f"Connected to mongodb")


    @log_function
    def close(self):
        self.__client.close()

    @log_function
    def insert_one(self, table_name: str, data: dict) -> ObjectId:
        try:
            self.logger.debug(f"Trying to insert data to table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].insert_one(data)
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
            res = self.__db[table_name].insert_many(data_list)
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
            res = self.__db[table_name].find_one(data_filter)
            if res:
                object_id = res.get('_id')
                self.logger.info(f"Got data from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return dict(res)
            else:
                desc = f"Error find data with filter: {data_filter}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.warning(desc)
                raise DataNotFoundDBException(desc)
        except Exception as e:
            self.logger.error(f"Error get one from db - {str(e)}")
            raise e

    @log_function
    def delete_one(self, table_name: str, data_filter: dict) -> bool:  # TODO: check
        try:
            self.logger.debug(f"Trying to delete one data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].delete_one(data_filter)
            if res and res.deleted_count>0:
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
    def delete_many(self, table_name: str, data_filter: dict) -> bool:
        try:
            self.logger.debug(f"Trying to delete collection of data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].delete_many(data_filter)
            if res.deleted_count and res.deleted_count>0:
                self.logger.info(
                    f"Deleted {res.deleted_count} records from db: '{self.DB_NAME}', " f"table_name: '{table_name}'")
                return True
            else:
                desc = f"Error delete data with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.error(desc)
                raise DeleteDataDBException(desc)
        except Exception as e:
            self.logger.error(f"Error delete many from db: {str(e)}")
            return False

    @log_function
    def update_one(self, table_name: str, data_filter: dict, new_data: dict) -> ObjectId:
        try:
            self.logger.debug(f"Trying to update one data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].update_one(data_filter, {"$set": new_data})
            if res:
                object_id = res.raw_result.get('_id')
                self.logger.info(
                    f"updated one data from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return object_id
            else:
                desc = f"Error update data with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.error(desc)
                raise UpdateDataDBException(desc)
        except Exception as e:
            self.logger.error(f"Error update one from db: {str(e)}")
            raise e

    @log_function
    def update_many(self, table_name: str, data_filter: dict, new_data: dict) -> List[ObjectId]:
        try:
            self.logger.debug(
                f"Trying to update {len(new_data)} records from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].update_many(data_filter, new_data)
            if res:
                object_id = res.raw_result.get('_id')
                self.logger.info(
                    f"updated {res.matched_count} records from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return object_id
            else:
                desc = f"Error update data with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.error(desc)
                raise UpdateDataDBException(desc)
        except Exception as e:
            self.logger.error(f"Error delete one from db: {str(e)}")
            raise e

    @log_function
    def count(self, table_name: str, data_filter: dict) -> int:
        try:
            self.logger.debug(
                f"Trying to count table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].count_documents(data_filter)
            if res and res > 0:
                self.logger.info(f"Counted {res} records from db: '{self.DB_NAME}', table_name: '{table_name}")
                return res
            else:
                desc = f"Didn't find record with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.debug(desc)
                return 0
        except Exception as e:
            self.logger.error(f"Error counting from db: {str(e)}")
            raise e

    @log_function
    def exists(self, table_name: str, data_filter: dict) -> bool:
        try:
            self.logger.debug(
                f"Trying to count table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.count(table_name, data_filter)
            if res and res > 0:
                # object_id = res.raw_result.get('_id')
                self.logger.info(
                    f"Found {res} in db: '{self.DB_NAME}', table_name: '{table_name}'")
                return True
            else:
                desc = f"Didn't find record with filter: {data_filter}, table: '{table_name}, db: {self.DB_NAME}'"
                self.logger.error(desc)
                return False
        except Exception as e:
            self.logger.error(f"Error counting from db: {str(e)}")
            return False

    @log_function
    def get_many(self, table_name: str, data_filter: dict) -> List[dict]:
        try:
            self.logger.debug(f"Trying to get one data from table: '{table_name}', db: '{self.DB_NAME}'")
            res = self.__db[table_name].find(data_filter)
            if res and res.retrieved>0:
                object_id = res.cursor_id
                self.logger.info(f"Got data from db: '{self.DB_NAME}', table_name: '{table_name}', id: '{object_id}'")
                return list(res)
            else:
                desc = f"Error find data with filter: {data_filter}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.error(desc)
                raise DataNotFoundDBException(desc)
        except Exception as e:
            self.logger.error(f"Error get many from db - {str(e)}")
            raise e
