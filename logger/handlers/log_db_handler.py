import logging
import os
from datetime import datetime

from pymongo import MongoClient

from logger.objects.log import Log
from server_utils.db_utils.validation_utils import get_mongodb_connection_string


class LogDBHandler(logging.Handler):
    DB_NAME = os.getenv(key='DB_NAME', default='local_restore')
    LOG_TABLE = "log"
    connection_string = None

    def _connect(self):
        self._connection_string = get_mongodb_connection_string()
        self.__client = MongoClient(self.connection_string)
        self.__db = self.__client[self.DB_NAME]

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
