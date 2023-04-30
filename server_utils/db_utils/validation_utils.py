import os
from typing import Tuple


def get_mongodb_connection_string() -> str:
    env_connection_string = os.getenv(key="CONNECTION_STRING")
    if not env_connection_string:
        db_password, db_url = get_password_and_db_name_validation_from_env()
        connection_string = f"mongodb+srv://allnews:{db_password}@{db_url}"
    else:
        connection_string = env_connection_string
    return connection_string


def get_password_and_db_name_validation_from_env() -> Tuple[str, str]:
    db_password = os.getenv(key="DB_PASSWORD")
    db_url = os.getenv(key="DB_URL")
    if not db_password or not db_url:
        raise ValueError(f"Cannot connect to db when DB_PASSWORD or DB_URL are None value or empty string")

    return db_password, db_url
