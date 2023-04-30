import datetime
import uuid

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.cluster import Cluster
from logger import log_function


@log_function
def create_new_cluster(article: Article) -> str:
    db = get_current_db_driver()
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
    db.update_one("clusters", {"cluster_id", cluster.cluster_id},
                  {"articles_id": cluster.articles_id, "websites": cluster.websites,
                   "last_updated": cluster.last_updated})
    db.update_one("articles", {"article_id", article.article_id}, {"cluster_id", cluster.cluster_id})
