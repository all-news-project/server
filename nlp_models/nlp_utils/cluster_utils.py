from db_driver import get_current_db_driver
from logger import get_current_logger, log_function
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import compare_text

"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


@log_function
def cluster_similarity(cluster_id: str, new_article_id: str) -> float:
    logger = get_current_logger()

    db = get_current_db_driver()
    cluster = db.get_one("clusters", {"cluster_id": cluster_id})
    new_article = db.get_one("articles", {"article_id", new_article_id})
    main_article = db.get_one("articles", {"article_id": cluster.main_article_id})
    sim_rate = compare_text([main_article.article_content, new_article.content])

    if sim_rate > 60:
        avg_rate = 0
        articles = db.get_many("articles", {"article_id": cluster.articles_id})
        for article in articles:
            avg_rate = avg_rate + compare_text([new_article, article.summary])
        avg_rate = avg_rate / len(articles)
        if sim_rate > 75 and avg_rate > 60:
            logger.debug(f"High similarity with article,average{avg_rate}")
        elif sim_rate > 60 and avg_rate > 70:
            logger.debug(f"Low similarity with article,average{avg_rate}")
        final_result=(avg_rate + sim_rate) / 2
        logger.debug(f"similarity rate to cluster is {final_result}")
        return final_result
    else:
        desc = f"Error Similarity rate {sim_rate}, Similarity not found"
        logger.debug(f"Similarity not found in {cluster.cluster_id}")
        raise SimilarityNotFoundException(desc)
