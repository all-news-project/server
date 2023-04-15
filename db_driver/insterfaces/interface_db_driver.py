from typing import List
from bson import ObjectId


class DBDriverInterface:
    def insert_one(self, table_name: str, data: dict) -> ObjectId:
        """
        Insert one data to db
        :param table_name:
        :param data:
        :return: object id of inserted data
        """
        raise NotImplementedError

    def insert_many(self, table_name: str, data_list: List[dict]) -> List[ObjectId]:
        """
        Insert many data to db
        :param table_name:
        :param data_list:
        :return: list of object ids of inserted data
        """
        raise NotImplementedError

    def get_one(self, table_name: str, data_filter: dict) -> dict:
        """
        Get one data from db
        :param table_name:
        :param data_filter:
        :return: wanted data
        """
        raise NotImplementedError

    def get_many(self, table_name: str, data_filter: dict) -> List[dict]:
        """
        Get many data from db
        :param table_name:
        :param data_filter:
        :return: list of wanted data
        """
        raise NotImplementedError

    def delete_one(self, table_name: str, data_filter: dict) -> bool:
        """
        Delete one data from db
        :param table_name:
        :param data_filter:
        :return: if the data was deleted
        """
        raise NotImplementedError

    def delete_many(self, table_name: str, data_filter: dict) -> int:
        """
        Delete many data from db
        :param table_name:
        :param data_filter:
        :return: count of data deleted
        """
        raise NotImplementedError

    def update_one(self, table_name: str, data_filter: dict, new_data: dict) -> ObjectId:
        """
        Update one data in db
        :param table_name:
        :param data_filter:
        :param new_data:
        :return: object id of updated data
        """
        raise NotImplementedError

    def update_many(self, table_name: str, data_filter: dict, new_data: dict) -> List[ObjectId]:
        """
        Update many data in db
        :param table_name:
        :param data_filter:
        :param new_data:
        :return: list of object ids of updated data
        """
        raise NotImplementedError

    def count(self, table_name: str, data_filter: dict) -> int:
        """
        Count data in db by data_filter
        :param table_name:
        :param data_filter:
        :return: count of data in table by data filter
        """
        raise NotImplementedError

    def exists(self, table_name: str, data_filter: dict) -> bool:
        """
        Check if data is exists in db by data_filter
        :param table_name:
        :param data_filter:
        :return: if the data is exists in table by data filter
        """
        raise NotImplementedError
