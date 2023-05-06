from db_driver.mongodb_driver import MongoDBDriver


def get_current_db_driver():
    """
    Singleton db driver
    :return:
    """
    return MongoDBDriver()
