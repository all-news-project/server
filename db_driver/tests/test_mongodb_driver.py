from datetime import datetime
from unittest import TestCase

from db_utils import get_current_db_driver, Article
from db_utils.db_objects.db_objects_utils import get_db_object_from_dict


def init_many():
    article_id = "article_test_id"
    url = 'test_article.com'
    website = 'cnn'
    title = "Test Article Title"
    content = "This is the content of the test article\nHappy Hanuka!\t\tThis is another line :-)!!!%%%\n*"
    publishing_time = datetime.now()
    collecting_time = datetime.now()
    test_articles = [Article(
        article_id=article_id + "1", url=url, website=website, title=title, content=content,
        publishing_time=publishing_time, collecting_time=collecting_time
    ),
        Article(
            article_id=article_id + "2", url=url, website=website, title=title, content=content,
            publishing_time=publishing_time, collecting_time=collecting_time
        ),
        Article(
            article_id=article_id + "3", url=url, website=website, title=title, content=content,
            publishing_time=publishing_time, collecting_time=collecting_time
        )
    ]
    return test_articles


def init_single():
    article_id = "article_test_id"
    url = 'test_article.com'
    website = 'cnn'
    title = "Test Article Title"
    content = "This is the content of the test article\nHappy Hanuka!\t\tThis is another line :-)!!!%%%\n*"
    publishing_time = datetime.now()
    collecting_time = datetime.now()
    test_article_single = Article(
        article_id=article_id, url=url, website=website, title=title, content=content,
        publishing_time=publishing_time, collecting_time=collecting_time
    )
    return test_article_single


class TestMongoDBUtils(TestCase):

    # TODO: add and fix tests
    def test_insert_one(self):
        try:
            db_utils = get_current_db_driver()
            article = init_single()

            return db_utils.insert_one(table_name='articles', data=article.convert_to_dict())
        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    def test_insert_many(self):
        try:

            db_utils = get_current_db_driver()
            articles = init_many()

            return db_utils.insert_many(table_name='articles',
                                        data_list=[article.convert_to_dict() for article in articles])

        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    def test_get_one(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_one()
            article = init_single()
            data_filter = {'article_id': article.article_id}
            article_dict = db_utils.get_one(table_name='articles', data_filter=data_filter)
            if not article_dict:
                self.fail()
            article = get_db_object_from_dict(object_dict=article_dict, class_instance=Article)
            print(article)

        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    # TODO:need to fix
    def test_get_many(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_many()
            articles = init_many()
            data_filter = {"article_id": {"$in": [article.article_id for article in articles]}}
            articles_dict = db_utils.get_many(table_name='articles',
                                              data_filter=data_filter)  # {"article_id": ids_to_find})
            if not articles_dict:
                self.fail()
            articles = get_db_object_from_dict(object_dict=articles_dict, class_instance=Article)
            print(articles)

        except Exception as e:
            print(f"test_insert_many: {e}")
            self.fail()

    def test_delete_one(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_one()
            article = init_single()
            data_filter = {'article_id': article.article_id}
            flag = db_utils.delete_one(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    def test_delete_many(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_many()
            articles = init_many()
            data_filter = {"article_id": {"$in": [article.article_id for article in articles]}}
            flag = db_utils.delete_many(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_many: {e}")
            self.fail()

    def test_exists(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_one()
            article = init_single()
            _id = self.test_insert_one()
            data_filter = {'article_id': article.article_id}
            flag = db_utils.exists(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    def test_count(self):
        try:
            db_utils = get_current_db_driver()
            self.test_insert_many()
            articles = init_many()
            data_filter = {"article_id": {"$in": [article.article_id for article in articles]}}
            flag = db_utils.count(table_name='articles', data_filter=data_filter)
            if flag == 0 or flag is None:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    # def test_update_one(self):
    #     try:
    #         db_utils = get_current_db_driver()
    #         _id = self.test_insert_one()
    #         data_filter = {'article_id': _id}
    #         flag = db_utils.update_one(table_name='articles', data_filter=data_filter)
    #         if not flag:
    #             self.fail()
    #     except Exception as e:
    #         print(f"test_delete_one: {e}")
    #         self.fail()
