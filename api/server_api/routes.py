from flask import request

from api.server_api import app
from api.server_api.api_logic import APILogic


@app.route('/')
def index():
    data = {"url": "all news"}
    return data


@app.route('/get_similar_articles', methods=['POST'])
def get_similar_articles():
    if 'url' in request.args:
        article_url: str = request.args['url']
        api_logic = APILogic()
        similar_articles_data = api_logic.get_similar_articles_data(article_url=article_url)
        if similar_articles_data:
            return similar_articles_data
        else:
            return "No articles found"
    else:
        return "Need to get current url"
