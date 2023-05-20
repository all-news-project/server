import datetime
import uuid

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import InsertDataDBException, UpdateDataDBException
from logger import log_function, get_current_logger
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.server_consts import ClusterConsts


class ClusterUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self.article_utils = ArticleUtils()

    @log_function
    def create_new_cluster(self, article: Article) -> str:
        for trie in range(ClusterConsts.TIMES_TRY_INSERT_CLUSTER):
            try:
                cluster_id = str(uuid.uuid4())
                cluster = Cluster(cluster_id=cluster_id, articles_id=[article.article_id],
                                  main_article_id=article.article_id,
                                  creation_time=datetime.datetime.now()
                                  , last_updated=datetime.datetime.now(), websites=[article.domain])
                _id = self._db.insert_one(table_name=DBConsts.CLUSTER_TABLE_NAME, data=cluster.convert_to_dict())
                self.logger.info(f"Inserted cluster inserted_id: `{_id}`, cluster_id: `{cluster.cluster_id}`")
                return _id
            except Exception as e:
                desc = f"Error insert cluster NO. {trie}/{ClusterConsts.TIMES_TRY_INSERT_CLUSTER} - {str(e)}"
                self.logger.warning(desc)

        desc = f"Error inserting article into db after {ClusterConsts.TIMES_TRY_INSERT_CLUSTER} tries"
        raise InsertDataDBException(desc)

    @log_function
    def add_article_to_cluster(self, cluster_id:str, article_id:str, article_domain:str):
        data_filter = {"cluster_id", cluster_id}
        data = {"articles_id": {"$addToSet": article_id}, "websites": {"$addToSet": article_domain},
                "last_updated": datetime.datetime.now()}
        for trie in range(ClusterConsts.TIMES_TRY_UPDATE_CLUSTER):
            try:
                self._db.update_one(table=DBConsts.CLUSTER_TABLE_NAME, data_filter=data_filter, data=data)
                self.article_utils.update_cluster_id(article_id=article_id, cluster_id=cluster_id)
                self.logger.info(f"Updated cluster cluster_id: `{cluster_id}`")
            except Exception as e:
                desc = f"Error insert article NO. {trie}/{ClusterConsts.TIMES_TRY_UPDATE_CLUSTER} - {str(e)}"
                self.logger.warning(desc)
                continue
        desc = f"Error inserting article into db after {ClusterConsts.TIMES_TRY_UPDATE_CLUSTER} tries"
        raise UpdateDataDBException(desc)
