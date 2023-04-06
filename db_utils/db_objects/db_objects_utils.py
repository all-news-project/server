import datetime

from db_utils import Article
from db_utils import get_current_db_driver
from nlp_models.nlp_utils.nlp_utils import summarize_text
import uuid

from logger import log_function



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
    db = get_current_db_driver()

    db.update_one("articles", {"article_id", article_id}, data)


@log_function
def create_article(url: str, title: str, content: str):
    db = get_current_db_driver()

    web_idx = url.find(".")
    _id = str(uuid.uuid4())
    website = url[:web_idx + 4]
    summ = summarize_text(content)
    article = Article(article_id=_id, url=url, website=website, title=title, content=content, summary=summ,
                      publishing_time=datetime.datetime.now())
    db.insert_one("articles", article)
    return _id


