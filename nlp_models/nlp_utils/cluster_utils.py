from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from db_driver.utils.consts import DBConsts
from logger import get_current_logger, log_function
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import compare_text

"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


@log_function
def cluster_similarity(cluster_id: str, new_article_id: str) -> float:
    logger = get_current_logger()

    db = get_current_db_driver()
    cluster = db.get_one(DBConsts.CLUSTER_TABLE_NAME, {"cluster_id": cluster_id})
    new_article = db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id", new_article_id})
    main_article = db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id": cluster.main_article_id})
    sim_rate = compare_text([main_article.article_content, new_article.content])

    if sim_rate > DBConsts.CLUSTER_LOW_SIM:
        avg_rate = _check_avg_cluster_sim(cluster, new_article)
        if sim_rate > DBConsts.CLUSTER_HIGH_SIM and avg_rate > DBConsts.CLUSTER_LOW_SIM:
            logger.debug(f"High similarity with article,average{avg_rate}")
        elif sim_rate > DBConsts.CLUSTER_LOW_SIM and avg_rate > DBConsts.CLUSTER_HIGH_SIM:
            logger.debug(f"Low similarity with article,average{avg_rate}")
        final_result = (avg_rate + sim_rate) / 2
        logger.debug(f"similarity rate to cluster is {final_result}")
        return final_result
    else:
        desc = f"Error Similarity rate {sim_rate}, Similarity not found"
        logger.debug(f"Similarity not found in {cluster.cluster_id}")
        raise SimilarityNotFoundException(desc)


@log_function
def _check_avg_cluster_sim(cluster: Cluster, new_article: Article):
    db = get_current_db_driver()
    avg_rate=0
    articles = db.get_many(DBConsts.ARTICLE_TABLE_NAME, {"article_id": cluster.articles_id})
    for article in articles:
        avg_rate = avg_rate + compare_text([new_article, article.summary])
    avg_rate = avg_rate / len(articles)
