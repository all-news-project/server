






"""This function searches every cluster in the database to find the best match for the current article
    by checking the similarity rate of every article in each cluster"""
from transformers import DistilBertTokenizer, DistilBertModel

from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from logger import get_current_logger, log_function
from nlp_models.nlp_utils.cluster_utils import cluster_similarity
from db_driver.utils.cluster_utils import create_new_cluster,update_cluster

logger = get_current_logger()


@log_function
def classify_article(clusters: list[Cluster], article: Article):
    # USE_CATEGORIAL_CLASSIFICATION = bool(os.getenv(key="USE_CATEGORIAL_CLASSIFICATION", default=False))
    counter = 0  # im adding this counter to check the number of clusters this subjects corresponds to for stats
    max_topic = None
    max_sim = 0
    for cluster in clusters:
        if article.website not in cluster.websites:
            logger.debug(f"checking similarity in cluster {cluster.cluster_id}")
            sim_rate = cluster_similarity(cluster, article)
            if sim_rate > max_sim:
                counter = counter + 1
                max_topic = cluster
                max_sim = sim_rate
    if max_sim > 0:
        # max_topic.articles_id.append(article.article_id)
        update_cluster(max_topic, article)
        # max_topic.add_article(article)
        logger.debug(f"Adding article to cluster {max_topic.cluster_id}")
    else:
        create_new_cluster(article)
        logger.debug("Could not find cluster, creating new cluster")
    # if counter > 1:
    #     pass
    # add an error log here to check why it corresponds to more than 1 topic


"""This function uses the DistilBert pretrained model by valurank in order to categorize articles."""


@log_function
def categorize_article(article: Article):
    logger.debug("Categorizing article")
    tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
    model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
    encoded_input = tokenizer.encode(article.content, return_tensors='pt')
    output = model(**encoded_input)
    logger.debug(f"Assigning category {output} to article {article.article_id}")
    return output


