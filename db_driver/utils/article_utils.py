import datetime

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from logger import log_function
import uuid
from nlp_models.nlp_utils.nlp_utils import summarize_text
from logger import get_current_logger

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
