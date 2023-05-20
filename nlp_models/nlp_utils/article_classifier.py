"""This function searches every cluster in the database to find the best match for the current article
    by checking the similarity rate of every article in each cluster"""
from transformers import DistilBertTokenizer, DistilBertModel

from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from logger import get_current_logger, log_function
from nlp_models.nlp_utils.cluster_utils import cluster_similarity
from server_utils.db_utils.cluster_utils import ClusterUtils


class ArticleClassifier:
    def __init__(self):
        self.logger = get_current_logger()
        self.cluster_utils = ClusterUtils()

    @log_function
    def classify_article(self, clusters: list[Cluster], article: Article) ->bool:
        logger = get_current_logger()
        counter = 0
        max_topic = None
        max_sim = 0
        for cluster in clusters:
            # TODO: check cluster websites
            if article.domain not in cluster.websites:
                logger.debug(f"checking similarity in cluster {cluster.cluster_id}")
                sim_rate = cluster_similarity(cluster.cluster_id, article.article_id)
                if sim_rate > max_sim:
                    counter = counter + 1
                    max_topic = cluster
                    max_sim = sim_rate
        if max_sim > 0:
            # max_topic.articles_id.append(article.article_id)
            self.cluster_utils.add_article_to_cluster(max_topic.cluster_id, article.article_id, article.domain)
            logger.info(f"Added article to cluster {max_topic.cluster_id}")
            return True
        else:
            try:
                logger.debug("Could not find cluster, creating new cluster")
                id = self.cluster_utils.create_new_cluster(article)
                return True
            except Exception as e:
                self.logger.error(f"Could not create new cluster - {str(e)}")
                return False


    """This function uses the DistilBert pretrained model by valurank in order to categorize articles."""

    @log_function
    def categorize_article(self, article: Article):
        logger = get_current_logger()
        try:
            logger.debug("Categorizing article")
            tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
            model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
            encoded_input = tokenizer.encode(article.content, return_tensors='pt')
            output = model(**encoded_input)
            logger.info(f"Assigning category {output} to article {article.article_id}")
            return output

        except Exception as e:
            logger.error(f"Failed to categorize article {article.article_id}")
            return None
