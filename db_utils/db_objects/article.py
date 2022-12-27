import datetime
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Article:
    article_id: str
    url: str
    website: str
    title: str
    content: str
    publishing_time: datetime.datetime
    collecting_time: datetime.datetime
    category: str = None
    images: List[str] = None
    state: str = None

    def __repr__(self):
        string = ''
        for attribute in [a for a in dir(self) if not a.startswith('__')]:
            string += f"{attribute}: {self.__getattribute__(attribute)}\n"
        return string

    def convert_to_dict(self):
        return asdict(self)


def get_article_from_dict(article_dict: dict) -> Article:
    article = Article(**article_dict)
    return article
