from db_utils.db_objects.article import Article
from db_utils.mongodb_utils import DBUtils


def get_current_db_driver():
    """
    Singleton db driver
    :return:
    """
    return DBUtils()
