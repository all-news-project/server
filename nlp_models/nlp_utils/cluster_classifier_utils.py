
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import NlpUtils
from db_driver import get_current_db_driver, DBConsts
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_utils.article_utils import ArticleUtils
from logger import get_current_logger, log_function


class ClusterClassifierUtils:
    def __init__(self):
        self._db = get_current_db_driver()
        self.logger = get_current_logger()
        self.article_utils = ArticleUtils()
        self.nlp = NlpUtils()

    @log_function
    def cluster_similarity(self, cluster: Cluster, new_article: Article) -> float:
        """
        This function is used to check the similarity between unclassified article and a specific cluster's articles
        """
        main_article = self.article_utils.get_article_by_id(article_id=cluster.main_article_id)
        sim_rate = self.nlp.compare_texts(main_article.content, new_article.content)
        if sim_rate > DBConsts.CLUSTER_HIGH_SIM:
            return sim_rate
        elif sim_rate > DBConsts.CLUSTER_LOW_SIM:
            avg_rate = self._check_avg_cluster_sim(cluster.articles_id, new_article)
            return avg_rate
        else:
            return 0


    @log_function
    def _check_avg_cluster_sim(self, article_ids: list[str], new_article: Article) -> float:
        avg_rate = 0
        articles = self._db.get_many(table_name=DBConsts.ARTICLES_TABLE_NAME,
                                     data_filter={"article_id": {"$in": article_ids}})
        for article in articles:
            avg_rate = avg_rate + self.nlp.compare_texts(new_article.content, article.content)
        return avg_rate / len(articles)
