import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

from server_utils.db_driver.utils.consts import DBObjectsConsts, DBConsts


@dataclass
class Article:
    article_id: str
    url: str
    domain: str
    title: str
    content: str
    collecting_time: datetime.datetime
    publishing_time: Optional[datetime.datetime] = None
    cluster_id: Optional[str] = None
    task_id: Optional[str] = None
    images: Optional[List[str]] = None

    def __repr__(self) -> str:
        string = f'(domain: `{self.domain}`, url: `{self.url}`, title: `{self.title}`)'
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)

    def convert_to_dict_for_json(self) -> dict:
        dict_object = self.convert_to_dict()
        date_time_attributes = DBObjectsConsts.DATETIME_ATTRIBUTES[DBConsts.ARTICLES_TABLE_NAME]
        for attribute_name in date_time_attributes:
            if dict_object[attribute_name]:
                dict_object[attribute_name] = dict_object[attribute_name].isoformat()
        return dict_object
