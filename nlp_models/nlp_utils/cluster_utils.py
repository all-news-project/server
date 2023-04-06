import datetime
import uuid

from db_utils.db_objects.cluster import Cluster
from logger import get_current_logger, log_function
from nlp_models.exceptions import SimilarityNotFoundException
from nlp_models.nlp_utils.nlp_utils import compare_text

logger = get_current_logger()
from db_utils import get_current_db_driver, Article


@log_function
def create_new_cluster(article: Article) -> str:
    db = get_current_db_driver()

    # new_cluster = Cluster(article)
    _id = str(uuid.uuid4())
    cluster = Cluster(_id, [article.article_id], article.article_id,
                      datetime.datetime.now()
                      , datetime.datetime.now(), [article.website])
    db.insert_one("clusters", cluster)
    return _id


@log_function
def update_cluster(cluster: Cluster, article: Article):
    db = get_current_db_driver()
    cluster.articles_id.append(article.article_id)
    article.cluster_id = cluster.cluster_id
    cluster.websites.append(article.website)
    cluster.last_updated = datetime.datetime.now()
    # db.update_one("clusters", {"cluster_id", cluster.cluster_id}, cluster)
    db.update_one("clusters", {"cluster_id", cluster.cluster_id},
                  {"articles_id": cluster.articles_id, "websites": cluster.websites,
                   "last_updated": cluster.last_updated})
    db.update_one("articles", {"article_id", article.article_id}, {"cluster_id", cluster.cluster_id})

"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


@log_function
def cluster_similarity(cluster: Cluster, new_article: Article) -> float:
    db = get_current_db_driver()

    main_article = db.get_one("articles", {"article_id": cluster.main_article_id})
    sim_rate = compare_text([main_article.article_content, new_article.content])

    if sim_rate > 60:
        avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
        articles = db.get_many("articles", {"article_id": cluster.articles_id})
        for article in articles:
            avg_rate = avg_rate + compare_text([new_article, article.summary])
        avg_rate = avg_rate / len(articles)
        if sim_rate > 75 and avg_rate > 60:
            logger.debug(f"High similarity with article,average{avg_rate}")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
        elif sim_rate > 60 and avg_rate > 70:
            logger.debug(f"Low similarity with article,average{avg_rate}")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
    # elif sim_rate > 60:
    #     avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
    #     for article in cluster.articles:
    #         avg_rate = avg_rate + compare_text([new_article, article.summary])
    #     avg_rate = avg_rate / len(cluster.articles)
    #     if avg_rate > 70:
    #         logger.debug("Low similarity with article , checking average")
    #         # self.add_article(newArticle)
    #         return (avg_rate + sim_rate) / 2
    else:
        desc = f"Error Similarity rate {sim_rate}, Similarity not found"
        logger.debug(f"Similarity not found in {cluster.cluster_id}")
        raise SimilarityNotFoundException(desc)  # TODO: add exception similarity not found
