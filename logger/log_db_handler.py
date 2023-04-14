import logging
import os
from datetime import datetime

from pymongo import MongoClient

from logger.objects.log import Log


class LogDBHandler(logging.Handler):
    DB_NAME = os.getenv(key='DB_NAME', default='local_restore')
    DB_PASSWORD = os.getenv(key='DB_PASSWORD')
    DB_URL = os.getenv(key='DB_URL')
    LOG_TABLE = "log"

    def _connect(self):
        self._check_password_and_db_name_validation()
        self.__client = MongoClient(f"mongodb+srv://allnews:{self.DB_PASSWORD}@{self.DB_URL}")
        self.__db = self.__client[self.DB_NAME]

    def _check_password_and_db_name_validation(self):
        if not self.DB_PASSWORD or not self.DB_URL:
            raise ValueError(f"Cannot connect to db when DB_PASSWORD or DB_URL are None value or empty string")

    def _disconnect(self):
        self.__client.close()

    def _insert(self, data: dict):
        try:
            self._connect()
            return self.__db[self.LOG_TABLE].insert_one(data)
        except Exception as e:
            raise e
        finally:
            self._disconnect()

    def emit(self, record: logging.LogRecord):
        try:
            data = {
                "level": record.levelname,
                "msg": self.format(record),
                "created": datetime.fromtimestamp(record.created),
                "task_id": record.task_id,
                "task_type": record.task_type
            }
            log = Log(**data)
            self._insert(log.convert_to_dict())
        except Exception as e:
            self.handleError(record)
