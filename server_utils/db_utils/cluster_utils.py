import uuid
from datetime import datetime
from typing import List

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import UpdateDataDBException
from logger import get_current_logger, log_function
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.server_consts import ClusterConsts


class ClusterUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self.article_utils = ArticleUtils()

    @log_function
    def create_new_cluster(self, article: Article, classified_categories: List[str] = None) -> str:
        try:
            current_time = datetime.now()
            categories = classified_categories if classified_categories else list()
            cluster_data = {
                "cluster_id": str(uuid.uuid4()),
                "articles_id": [article.article_id],
                "main_article_id": article.article_id,
                "creation_time": current_time,
                "last_updated": current_time,
                "domains": [article.domain],
                "categories": categories
            }
            cluster: Cluster = Cluster(**cluster_data)
            _id = self._db.insert_one(table_name=DBConsts.CLUSTERS_TABLE_NAME, data=cluster.convert_to_dict())
            self.logger.info(f"Inserted cluster inserted_id: `{_id}`, cluster_id: `{cluster.cluster_id}`")
            return _id
        except Exception as e:
            desc = f"Error insert cluster - {str(e)}"
            self.logger.exception(desc)

    def get_cluster(self, cluster_id: str) -> Cluster:
        data_filter = {"cluster_id": cluster_id}
        cluster_data = self._db.get_one(table_name=DBConsts.CLUSTERS_TABLE_NAME, data_filter=data_filter)
        cluster_object: Cluster = get_db_object_from_dict(object_dict=cluster_data, class_instance=Cluster)
        return cluster_object

    def get_clusters(self, different_domain: str = None, category: List[str] = None) -> List[Cluster]:
        clusters: List[Cluster] = list()
        data_filter = dict()
        if different_domain:
            data_filter = {"domains": {"$nin": [different_domain]}}
        if category:
            data_filter.update({"categories": {"$in": category}})
        clusters_dicts = self._db.get_many(table_name=DBConsts.CLUSTERS_TABLE_NAME, data_filter=data_filter)
        for cluster_dict in clusters_dicts:
            cluster: Cluster = get_db_object_from_dict(object_dict=cluster_dict, class_instance=Cluster)
            clusters.append(cluster)
        return clusters

    @log_function
    def add_article_to_cluster(self, cluster_id: str, article_id: str, article_domain: str):
        data_filter = {"cluster_id", cluster_id}
        data = {"articles_id": {"$addToSet": article_id}, "websites": {"$addToSet": article_domain},
                "last_updated": datetime.now()}
        for trie in range(ClusterConsts.TIMES_TRY_UPDATE_CLUSTER):
            try:
                self._db.update_one(table=DBConsts.CLUSTERS_TABLE_NAME, data_filter=data_filter, data=data)
                self.article_utils.update_cluster_id(article_id=article_id, cluster_id=cluster_id)
                self.logger.info(f"Updated cluster cluster_id: `{cluster_id}`")
            except Exception as e:
                desc = f"Error insert article NO. {trie}/{ClusterConsts.TIMES_TRY_UPDATE_CLUSTER} - {str(e)}"
                self.logger.warning(desc)
                continue
        desc = f"Error inserting article into db after {ClusterConsts.TIMES_TRY_UPDATE_CLUSTER} tries"
        raise UpdateDataDBException(desc)


# For debug
if __name__ == '__main__':
    article_utils = ArticleUtils()
    new_article: Article = article_utils.get_article_by_url(article_url="https://www.bbc.com/news/world-europe-65471904")
    cluster_utils = ClusterUtils()
    cluster_utils.create_new_cluster(article=new_article, classified_categories=["finance", "bitcoin"])

