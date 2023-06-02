import random
from typing import List

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import InsertDataDBException, UpdateDataDBException
from logger import get_current_logger
from server_utils.server_consts import ArticleConsts


class ArticleUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()

    def insert_article(self, article: Article):
        for trie in range(ArticleConsts.TIMES_TRY_INSERT_ARTICLE):
            try:
                obj_id = self._db.insert_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data=article.convert_to_dict())
                self.logger.info(f"Inserted article inserted_id: `{obj_id}`, article_id: `{article.article_id}`")
                return
            except Exception as e:
                desc = f"Error insert article NO. {trie}/{ArticleConsts.TIMES_TRY_INSERT_ARTICLE} - {str(e)}"
                self.logger.warning(desc)
                continue
        desc = f"Error inserting article into db after {ArticleConsts.TIMES_TRY_INSERT_ARTICLE} tries"
        raise InsertDataDBException(desc)

    def update_cluster_id(self, article_id: str, cluster_id: str):
        for trie in range(ArticleConsts.TIMES_TRY_UPDATE_CLUSTER_ID):
            try:
                data_filter = {"article_id": article_id}
                new_data = {"cluster_id": cluster_id}
                self._db.update_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter, new_data=new_data)
                self.logger.info(f"Updated article article_id: `{article_id}`")
                return
            except Exception as e:
                desc = f"Error insert article NO. {trie}/{ArticleConsts.TIMES_TRY_INSERT_ARTICLE} - {str(e)}"
                self.logger.warning(desc)
                continue
        desc = f"Error inserting article into db after {ArticleConsts.TIMES_TRY_INSERT_ARTICLE} tries"
        raise UpdateDataDBException(desc)

    def get_unclassified_article(self, required_filter_data: dict = None, get_random: bool = False) -> Article:
        data_filter = {"cluster_id": None}
        if required_filter_data:
            data_filter.update(required_filter_data)

        if get_random:
            articles = self._db.get_many(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)
            article = random.choice(articles)
        else:
            # todo: check the order of the collecting article
            article = self._db.get_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)

        return Article(**article)

    def get_article(self, article_url: str) -> Article:
        data_filter = {"url": article_url}
        article_data = self._db.get_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)
        article_object: Article = get_db_object_from_dict(object_dict=article_data, class_instance=Article)
        return article_object

    def get_articles(self, articles_id: List[str]) -> List[Article]:
        articles: List[Article] = []
        data_filter = {"article_id": {"$in": articles_id}}
        articles_data = self._db.get_many(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)
        for article_data in articles_data:
            articles.append(get_db_object_from_dict(object_dict=article_data, class_instance=Article))
        return articles
