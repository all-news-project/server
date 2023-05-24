from flask import request

from api.server_api import app


@app.route('/')
def index():
    data = {"url": "all news"}
    return data


@app.route('/get_similar_articles', methods=['POST'])
def get_similar_articles():
    if 'url' in request.args:
        # todo: check in cluster db
        article_url: str = request.args['url']
        return {"similar": ["similar 1", "similar 2"], "article_url": article_url}
    else:
        return "Need to get current url"
