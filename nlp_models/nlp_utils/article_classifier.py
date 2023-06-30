import os
from time import sleep
from typing import List
from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import DataNotFoundDBException
from logger import get_current_logger, log_function
from nlp_models.nlp_utils.cluster_classifier_utils import ClusterClassifierUtils
from nlp_models.nlp_utils.nlp_utils import NlpUtils
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.db_utils.cluster_utils import ClusterUtils
from server_utils.server_consts import ScheduleConsts


class ArticleClassifier:
    USE_CATEGORIZED = bool(os.getenv(key="USE_CATEGORIZED", default=False))

    def __init__(self):
        # drivers
        self.logger = get_current_logger()
        self._db = get_current_db_driver()

        # utils
        self.cluster_utils = ClusterUtils()
        self.article_utils = ArticleUtils()
        self.cluster_nlp = ClusterClassifierUtils()
        self.nlp_utils = NlpUtils()

    @log_function
    def classify_article(self, clusters: list[Cluster], article: Article, category: List[str] = None) -> bool:
        counter = 0
        max_sim = 0
        match_cluster = None
        for cluster in clusters:
            self.logger.debug(f"checking similarity in cluster {cluster.cluster_id}")
            sim_rate_with_cluster = self.cluster_nlp.cluster_similarity(cluster, article)
            if sim_rate_with_cluster > max_sim:
                counter = counter + 1
                match_cluster = cluster
                max_sim = sim_rate_with_cluster

        if max_sim > DBConsts.CLUSTER_THRESHOLD:
            self.cluster_utils.add_article_to_cluster(match_cluster.cluster_id, article.article_id, article.domain)
            self.logger.info(f"Added article to cluster {match_cluster.cluster_id}")
        else:
            try:
                self.logger.debug("Could not find cluster, creating new cluster")
                self.cluster_utils.create_new_cluster(article=article, classified_categories=category)
                return True
            except Exception as e:
                self.logger.error(f"Could not create new cluster - {str(e)}")

    @log_function
    def run(self):
        """
        This function searches every cluster in the database to find the best match for the current article
        by checking the similarity rate of every article in each cluster
        """
        while True:
            category = None
            try:
                new_article: Article = self.article_utils.get_unclassified_article()
                if self.USE_CATEGORIZED:
                    # todo: @Tal - check if `categorize_article` return str or list, if fail return None??
                    category = self.nlp_utils.categorize_article(new_article.content)
                    clusters = self.cluster_utils.get_clusters(different_domain=new_article.domain, category=category)
                    self.logger.debug(f"Got clusters from category - {category}")
                else:
                    clusters = self.cluster_utils.get_clusters(different_domain=new_article.domain)
                    self.logger.debug("Getting all the clusters")

                self.classify_article(clusters, new_article, category)

            except DataNotFoundDBException:
                self.logger.warning(f"Couldn't find article, sleeping for {ScheduleConsts.SLEEPING_TIME / 60} minutes")
                sleep(ScheduleConsts.SLEEPING_TIME)
            except Exception as e:
                self.logger.warning(f"Error handle Article clustering - {str(e)}")
