import datetime

from db_utils import Article
from db_utils.db_objects.cluster import Cluster
from db_utils import get_current_db_driver
from nlp_models.nlp_utils import summarize_text
import os
import uuid

from logger import log_function

db = get_current_db_driver()


def get_db_object_from_dict(object_dict: dict, class_instance) -> object:
    """
    Getting a database dictionary and a class and return the database object

    # example of use:
    article = get_db_object_from_dict(object_dict=article_dict, class_instance=Article)

    :param object_dict:
    :param class_instance:
    :return:
    """
    if "_id" in object_dict.keys():
        object_dict.pop("_id", None)
    obj = class_instance(**object_dict)
    return obj


def update_article(article_id: str, data: dict):
    db.update_one("articles", {"article_id", article_id}, data)


@log_function
def create_article(url: str, title: str, content: str):
    web_idx = url.find(".")
    _id = str(uuid.uuid4())
    website = url[:web_idx + 4]
    summ = summarize_text(content)
    article = Article(article_id=_id, url=url, website=website, title=title, content=content, summary=summ,
                      publishing_time=datetime.datetime.now())
    db.insert_one("articles", article)
    return _id


@log_function
def create_new_cluster(article: Article):
    # new_cluster = Cluster(article)
    _id = str(uuid.uuid4())
    cluster = Cluster(_id, [article.article_id], article.summary, article.title, article.content,
                      datetime.datetime.now()
                      , datetime.datetime.now(), [article.website])
    db.insert_one("clusters", cluster)
    return _id


@log_function
def update_cluster(cluster: Cluster, article: Article):
    cluster.articles_id.append(article.article_id)
    article.cluster_id = cluster.cluster_id
    cluster.websites.append(article.website)
    cluster.last_updated = datetime.datetime.now()
    # db.update_one("clusters", {"cluster_id", cluster.cluster_id}, cluster)
    db.update_one("clusters", {"cluster_id", cluster.cluster_id},
                  {"articles_id": cluster.articles_id, "websites": cluster.websites,
                   "last_updated": cluster.last_updated})
    db.update_one("articles", {"article_id", article.article_id}, {"cluster_id", cluster.cluster_id})
