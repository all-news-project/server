import datetime
import uuid

from db_utils.db_objects.cluster import Cluster
from logger import get_current_logger, log_function
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import compare_text

# logger = get_current_logger()
from db_utils import get_current_db_driver, Article


@log_function
def create_new_cluster(article: Article) -> str:
    logger = get_current_logger()

    db = get_current_db_driver()
    # new_cluster = Cluster(article)
    _id = str(uuid.uuid4())
    cluster = Cluster(_id, [article.article_id], article.article_id,
                      datetime.datetime.now()
                      , datetime.datetime.now(), [article.website])
    try:
        db.insert_one("clusters", cluster)
        logger.info(f"Successfully added cluster {cluster.cluster_id} to db")
        return _id
    except Exception as e:
        logger.error("Failed to add cluster to db")
        print(e)
        return None
    # return _id


@log_function
def update_cluster(cluster: Cluster, article: Article, data_filter=None, new_data=None):
    logger = get_current_logger()

    db = get_current_db_driver()
    if new_data is None:
        cluster.articles_id.append(article.article_id)
        article.cluster_id = cluster.cluster_id
        cluster.websites.append(article.website)
        cluster.last_updated = datetime.datetime.now()
        new_data = {"articles_id": cluster.articles_id, "websites": cluster.websites,
                    "last_updated": cluster.last_updated}
    # db.update_one("clusters", {"cluster_id", cluster.cluster_id}, cluster)
    if data_filter is None:
        data_filter = {"cluster_id", cluster.cluster_id}
    try:
        db.update_one(table_name="clusters", data_filter=data_filter,
                      new_data=new_data)
        logger.debug(f"updated cluster {cluster.cluster_id}")
    except Exception as e:
        logger.error(f"failed to update cluster {cluster.cluster_id}")
    try:
        db.update_one("articles", {"article_id", article.article_id}, {"cluster_id", cluster.cluster_id})
        logger.debug(f"updated article {cluster.articles_id}")
    except Exception as e:
        logger.error(f"failed to update cluster {article.article_id}")


"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


@log_function
def cluster_similarity(cluster_id: str, new_article_id: str) -> float:
    logger = get_current_logger()

    db = get_current_db_driver()
    cluster=db.get_one("clusters",{"cluster_id":cluster_id})
    new_article=db.get_one("articles",{"article_id",new_article_id})
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
