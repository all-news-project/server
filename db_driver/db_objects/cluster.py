from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Optional


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
