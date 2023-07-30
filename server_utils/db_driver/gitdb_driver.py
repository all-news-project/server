import os
from datetime import datetime
from typing import List

import requests
from bson import ObjectId

from server_utils.db_driver.insterfaces.interface_db_driver import DBDriverInterface
from server_utils.db_driver.utils.consts import DBConsts, DBObjectsConsts
from server_utils.db_driver.utils.exceptions import ErrorConnectDBException, DataNotFoundDBException
from server_utils.logger import log_function, get_current_logger
from server_utils.singleton_class import Singleton


class GitDBDriver(DBDriverInterface, Singleton):
    DB_NAME = os.getenv(key='DB_NAME', default='git')

    def __init__(self):
        self.logger = get_current_logger()
        self.__connect_to_db()
        self.logger.debug(f"Connected to gitdb")

    def __connect_to_db(self):
        self.__db = dict()
        for collection in DBConsts.GIT_DB_COLLECTIONS:
            try:
                self.logger.debug(msg=f"Trying to get db data for `{collection}`")
                res = requests.get(f"{DBConsts.GIT_DB_URL}{collection}.json")
                res_json = res.json()
                date_time_attributes = DBObjectsConsts.DATETIME_ATTRIBUTES[collection]
                for document in res_json:
                    for date_time_attribute in date_time_attributes:
                        if document[date_time_attribute] and isinstance(document[date_time_attribute], str):
                            document[date_time_attribute] = datetime.fromisoformat(document[date_time_attribute])
                self.__db[collection] = res_json
                self.logger.info(f"Done collect data from git db for `{collection}`, Got {len(res_json)}")
            except Exception as e:
                desc = f"Error getting git db data for `{collection}`, except: {str(e)}"
                self.logger.error(desc)
                raise ErrorConnectDBException(desc)

    @log_function
    def get_one(self, table_name: str, data_filter: dict) -> dict:
        try:
            self.logger.debug(f"Trying to get one data from table: '{table_name}', db: '{self.DB_NAME}'")
            for document in self.__db[table_name]:
                for key, value in data_filter.items():
                    if document[key] and document[key] == value:
                        self.logger.info(f"Got data from db: '{self.DB_NAME}', table_name: '{table_name}''")
                        return document

            desc = f"Error find data with filter: {data_filter}, table: '{table_name}', db: '{self.DB_NAME}'"
            self.logger.warning(desc)
            raise DataNotFoundDBException(desc)
        except Exception as e:
            self.logger.error(f"Error get one from db - {str(e)}")
            raise e

    @log_function
    def get_many(self, table_name: str, data_filter: dict) -> List[dict]:
        try:
            self.logger.debug(f"Trying to get one data from table: '{table_name}', db: '{self.DB_NAME}'")
            documents = []
            for document in self.__db[table_name]:
                for key, value in data_filter.items():
                    if not document[key]:
                        continue
                    if isinstance(value, dict):
                        if "$in" in value.keys():
                            if any([document[key] == single_value for single_value in value["$in"]]):
                                documents.append(document)
                    elif document[key] == value:
                        documents.append(document)

            if documents:
                self.logger.info(f"Got {len(documents)} data from db: '{self.DB_NAME}', table_name: '{table_name}'")
                return documents
            else:
                desc = f"Error find data with filter: {data_filter}, table: '{table_name}', db: '{self.DB_NAME}'"
                self.logger.warning(desc)
                raise DataNotFoundDBException(desc)
        except Exception as e:
            self.logger.error(f"Error get one from db - {str(e)}")
            raise e

    @log_function
    def count(self, table_name: str, data_filter: dict) -> int:
        try:
            return len(self.get_many(table_name=table_name, data_filter=data_filter))
        except DataNotFoundDBException:
            return 0

    @log_function
    def exists(self, table_name: str, data_filter: dict) -> bool:
        try:
            return self.get_one(table_name=table_name, data_filter=data_filter) is not None
        except DataNotFoundDBException:
            return False

    @log_function
    def delete_one(self, table_name: str, data_filter: dict) -> bool:
        raise NotImplementedError(DBConsts.GIT_DB_DELETE_ERROR_MSG)

    @log_function
    def delete_many(self, table_name: str, data_filter: dict) -> int:
        raise NotImplementedError(DBConsts.GIT_DB_DELETE_ERROR_MSG)

    def insert_one(self, table_name: str, data: dict) -> ObjectId:
        raise NotImplementedError(DBConsts.GIT_DB_INSERT_ERROR_MSG)

    def insert_many(self, table_name: str, data_list: List[dict]) -> List[ObjectId]:
        raise NotImplementedError(DBConsts.GIT_DB_INSERT_ERROR_MSG)

    def update_one(self, table_name: str, data_filter: dict, new_data: dict) -> ObjectId:
        raise NotImplementedError(DBConsts.GIT_DB_UPDATE_ERROR_MSG)

    def update_many(self, table_name: str, data_filter: dict, new_data: dict) -> List[ObjectId]:
        raise NotImplementedError(DBConsts.GIT_DB_UPDATE_ERROR_MSG)
