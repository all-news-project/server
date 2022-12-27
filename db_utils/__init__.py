from datetime import datetime
from functools import cache
from uuid import uuid4

from db_utils.db_objects.article import Article
from db_utils.mongodb_utils import MongoDBUtils


@cache
def get_current_db_driver():
    """
    Singleton db driver
    :return:
    """
    return MongoDBUtils()


if __name__ == '__main__':
    # example
    db_utils = get_current_db_driver()
    # article_id = str(uuid4())
    # url = 'test_article.com'
    # website = 'cnn'
    # title = "Test Article Title"
    # content = "This is the content of the test article\nHappy Hanuka!\t\tThis is another line :-)!!!%%%\n*"
    # publishing_time = datetime.now()
    # collecting_time = datetime.now()
    # test_article = Article(
    #     article_id=article_id, url=url, website=website, title=title, content=content, publishing_time=publishing_time,
    #     collecting_time=collecting_time
    # )
    # db_utils.insert(table_name='articles', data=test_article.convert_to_dict())
    data = db_utils.get_one(table_name='articles', data_filter={'article_id': '05504dac-cb0f-410c-bce4-713482a59e42'})
    print(data)
