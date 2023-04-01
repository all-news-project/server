from datetime import datetime
from dataclasses import asdict
from typing import Optional

from nlp_models.model_two import genis
from db_utils import Article


# just a thought, we can add machine learning model to learn the best similarity rates to get the best clustering

class Cluster:
    articles: list[Article]
    summary: str
    title: str
    article_content: str
    creation_time: datetime
    last_updated: datetime
    category: Optional[str] = None
    websites: list[str]
    #similizer: Optional[nlp_similizer] = None  # not necessary but i want to check whether the model have any significance

    def __init__(self, newArticle: Article):
        self.articles = [newArticle]
        # TODO: self.summary = need to add summarizer (Tal already written one for previous job offer)
        self.title = newArticle.title
        self.article_content = newArticle.content
        self.creation_time = datetime.now()
        self.last_updated = datetime.now()
        # TODO: self.category = need to add nlp article classifier
        self.websites = [newArticle.website]

    # def add_article(self, article: Article):
    #     try:
    #         self.articles.append(article)
    #         self.last_updated = datetime.now()
    #         self.websites.append(article.website)
    #         # TODO: add to db / update cluster
    #     except:
    #         pass  # TODO : add logging here

    # TODO: move to nlp_utils


    # def convert_to_dict(self) -> dict:
    #     return asdict(self)
