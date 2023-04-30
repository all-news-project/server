import datetime

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from logger import log_function
import uuid
from nlp_models.nlp_utils.nlp_utils import summarize_text


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

