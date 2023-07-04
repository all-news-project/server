from flask import request

from server_api import app
from server_api.api_logic import APILogic
from server_api.exceptions import ArticleNotFoundException, NoSimilarArticlesException, GetSimilarArticlesException
from server_utils.logger import get_current_logger


@app.route('/')
def index():
    data = {"url": "all news"}
    return data


@app.route('/get_similar_articles', methods=['POST'])
def get_similar_articles():
    logger = get_current_logger()
    logger.debug(f"Try getting similar articles")
    return_data = {"articles_data": list(), "error_msg": "", "succeeded": False}
    if 'url' not in request.args:
        return_data["error_msg"] = "url required"
        logger.logger.warning(f"Didn't get the current url of the article")
    else:
        try:
            api_logic = APILogic()
            article_url: str = request.args['url']
            similar_articles_data = api_logic.get_similar_articles_data(article_url=article_url)
            return_data["articles_data"] = similar_articles_data
            return_data["succeeded"] = True
            logger.info(f"Got {len(similar_articles_data)} similar articles")
        except ArticleNotFoundException:
            return_data["error_msg"] = "article not found in db"
        except NoSimilarArticlesException:
            return_data["error_msg"] = "no similar articles found"
        except GetSimilarArticlesException:
            return_data["error_msg"] = "error getting similar articles"

    logger.info(f"(get_similar_articles) return data: `{return_data}`")
    return return_data
