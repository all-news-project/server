"""This function searches every cluster in the database to find the best match for the current article
    by checking the similarity rate of every article in each cluster"""
from time import sleep

from transformers import DistilBertTokenizer, DistilBertModel

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
from logger import get_current_logger, log_function
from nlp_models.nlp_utils.cluster_utils import ClusterNlp
from server_utils.db_utils.cluster_utils import ClusterUtils
from server_utils.server_consts import ScheduleConsts


class ArticleClassifier:
    def __init__(self):
        self.logger = get_current_logger()
        self.cluster_utils = ClusterUtils()
        self.cluster_nlp = ClusterNlp()
        self._db = get_current_db_driver()

    @log_function
    def classify_article(self, clusters: list[Cluster], article: Article) -> bool:
        counter = 0
        max_topic = None
        max_sim = 0
        for cluster in clusters:
            # TODO: check cluster websites
            if article.domain not in cluster.websites:
                self.logger.debug(f"checking similarity in cluster {cluster.cluster_id}")
                sim_rate = self.cluster_nlp.cluster_similarity(cluster.cluster_id, article.article_id)
                if sim_rate > max_sim:
                    counter = counter + 1
                    max_topic = cluster
                    max_sim = sim_rate
        if max_sim > 0:
            # max_topic.articles_id.append(article.article_id)
            self.cluster_utils.add_article_to_cluster(max_topic.cluster_id, article.article_id, article.domain)
            self.logger.info(f"Added article to cluster {max_topic.cluster_id}")
            return True
        else:
            try:
                self.logger.debug("Could not find cluster, creating new cluster")
                id = self.cluster_utils.create_new_cluster(article)
                return True
            except Exception as e:
                self.logger.error(f"Could not create new cluster - {str(e)}")
                return False

    """This function uses the DistilBert pretrained model by valurank in order to categorize articles."""

    @log_function
    def categorize_article(self, article: Article):
        # logger = get_current_logger()
        try:
            self.logger.debug("Categorizing article")
            tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
            model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
            encoded_input = tokenizer.encode(article.content, return_tensors='pt')
            output = model(**encoded_input)
            self.logger.info(f"Assigning category {output} to article {article.article_id}")
            return output

        except Exception as e:
            self.logger.error(f"Failed to categorize article {article.article_id}")
            return None

    @log_function
    def run(self):
        data_filter = {"cluster_id": None}
        categorized = True
        clusters_dict = []
        while True:
            try:
                new_article = Article(
                    **self._db.get_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter))
                if new_article:
                    if categorized:
                        article_category = self.categorize_article(new_article)
                        data_filter = {"category": article_category}
                        clusters_dict = self._db.get_many(table_name=DBConsts.CLUSTER_TABLE_NAME,
                                                          data_filter=data_filter)
                        self.logger.debug(f"Getting clusters from category - {article_category}")
                    else:
                        clusters_dict = self._db.get_many(table_name=DBConsts.CLUSTER_TABLE_NAME)
                        self.logger.debug("Getting all the clusters")
                    clusters = [get_db_object_from_dict(cluster, Cluster) for cluster in clusters_dict]
                    self.classify_article(clusters, new_article)
                else:
                    self.logger.warning(
                        f"Couldn't find article, sleeping for {ScheduleConsts.SLEEPING_TIME / 60} minutes")
                    sleep(ScheduleConsts.SLEEPING_TIME)

            except Exception as e:
                self.logger.warning(f"Error handle Article clustering - {str(e)}")
