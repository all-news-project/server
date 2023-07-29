import os

from server_utils.db_driver.gitdb_driver import GitDBDriver
from server_utils.db_driver.mongodb_driver import MongoDBDriver
from server_utils.db_driver.utils.consts import DBConsts

DB_INSTANCES = dict()


def get_current_db_driver():
    """
    Return db driver
    :return:
    """
    db_name = os.getenv(key='DB_NAME')
    if db_name == DBConsts.GIT_DB_NAME:
        if db_name not in DB_INSTANCES.keys():
            DB_INSTANCES[db_name] = GitDBDriver()
        return DB_INSTANCES[db_name]
    else:
        return MongoDBDriver()
