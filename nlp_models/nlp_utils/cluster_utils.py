from logger import log_function
from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.utils.consts import DBConsts
from logger import get_current_logger, log_function
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import Nlp_Utils

"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


class ClusterNlp:
    def __init__(self):
        self._db = get_current_db_driver()
        self.logger = get_current_logger()
        self.nlp = Nlp_Utils()

    @log_function
    def cluster_similarity(self, cluster_id: str, new_article_id: str) -> float:
        cluster = self._db.get_one(DBConsts.CLUSTER_TABLE_NAME, {"cluster_id": cluster_id})
        new_article = self._db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id", new_article_id})
        main_article = self._db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id": cluster.main_article_id})
        sim_rate = self.nlp.compare_text([main_article.article_content, new_article.content])
        if sim_rate > DBConsts.CLUSTER_LOW_SIM:
            avg_rate = self._check_avg_cluster_sim(cluster.articles_id, new_article)
            if sim_rate > DBConsts.CLUSTER_HIGH_SIM and avg_rate > DBConsts.CLUSTER_LOW_SIM:
                self.logger.debug(f"High similarity with article,average {avg_rate}")
            elif sim_rate > DBConsts.CLUSTER_LOW_SIM and avg_rate > DBConsts.CLUSTER_HIGH_SIM:
                self.logger.debug(f"Low similarity with article,average {avg_rate}")
            final_result = (avg_rate + sim_rate) / 2
            self.logger.debug(f"similarity rate to cluster is {final_result}")
            return final_result
        else:
            desc = f"Error Similarity rate {sim_rate}, Similarity not found"
            self.logger.debug(f"Similarity not found in {cluster.cluster_id}")
            raise SimilarityNotFoundException(desc)

    @log_function
    def _check_avg_cluster_sim(self, article_ids: list[str], new_article: Article) -> float:
        avg_rate = 0
        articles = self._db.get_many(DBConsts.ARTICLE_TABLE_NAME, {"article_id": article_ids})
        for article in articles:
            avg_rate = avg_rate + self.nlp.compare_text([new_article, article.content])
        return avg_rate / len(articles)
