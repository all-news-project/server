import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

#from db_driver.db_objects.cluster import Cluster


@dataclass
class Article:
    article_id: str
    url: str
    website: str
    title: str
    content: str
    summary: str
    publishing_time: datetime.datetime
    collecting_time: datetime.datetime = None
    cluster_id: str = None
    category: Optional[str] = None
    images: Optional[List[str]] = None
    state: Optional[str] = None
    task_id: str = None

    def __repr__(self) -> str:
        string = ''
        for prop, value in vars(self).items():
            string += f"{str(prop)}: {str(value)}\n"
        return string

    def convert_to_dict(self) -> dict:
        return asdict(self)
