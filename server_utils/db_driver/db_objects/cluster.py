from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Optional

from server_utils.db_driver.utils.consts import DBObjectsConsts, DBConsts


@dataclass
class Cluster:
    cluster_id: str
    articles_id: list[str]
    main_article_id: str
    creation_time: datetime
    last_updated: datetime
    domains: list[str]
    categories: Optional[str] = None

    def convert_to_dict(self) -> dict:
        return asdict(self)
    
    def convert_to_dict_for_json(self) -> dict:
        dict_object = self.convert_to_dict()
        date_time_attributes = DBObjectsConsts.DATETIME_ATTRIBUTES[DBConsts.CLUSTERS_TABLE_NAME]
        for attribute_name in date_time_attributes:
            if dict_object[attribute_name]:
                dict_object[attribute_name] = dict_object[attribute_name].isoformat()
        return dict_object
