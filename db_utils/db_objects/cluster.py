from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Optional

from nlp_models.model_two import genis
from db_utils import Article


# just a thought, we can add machine learning model to learn the best similarity rates to get the best clustering

@dataclass
class Cluster:
    cluster_id: str
    articles_id: list[str]
    summary: str
    title: str
    article_content: str
    creation_time: datetime
    last_updated: datetime
    websites: list[str]
    category: Optional[str] = None

    def convert_to_dict(self) -> dict:
        return asdict(self)
