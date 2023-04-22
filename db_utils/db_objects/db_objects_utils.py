import datetime

from db_utils import Article
from db_utils import get_current_db_driver
from nlp_models.nlp_utils.nlp_utils import summarize_text
import uuid

from logger import log_function, get_current_logger


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
    logger = get_current_logger()

    try:
        db.update_one("articles", {"article_id", article_id}, data)
        logger.debug(f"Successfully updated article {article_id}")
    except Exception as e:
        logger.error(f"Failed to update article {article_id}")
        print(e)



@log_function
def create_article(url: str, title: str, content: str) -> object:
    db = get_current_db_driver()
    logger = get_current_logger()
    web_idx = url.find(".")
    _id = str(uuid.uuid4())
    website = url[:web_idx + 4]
    summ = summarize_text(content)
    try:
        article = Article(article_id=_id, url=url, website=website, title=title, content=content, summary=summ,
                          publishing_time=datetime.datetime.now())
        db.insert_one("articles", article)
        logger.debug(f"Successfully added article {article.title} to db")
    except Exception as e:
        logger.error("Failed to add article to db")
        print(e)
        # TODO: need to check if already doing so.
    return _id
