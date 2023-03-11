from datetime import datetime
from unittest import TestCase

from db_utils import get_current_db_driver, Article
from db_utils.db_objects.db_objects_utils import get_db_object_from_dict


class TestMongoDBUtils(TestCase):
    # TODO: add and fix tests
    def test_insert_one(self):
        try:
            db_utils = get_current_db_driver()
            article_id = "article_test_id"
            url = 'test_article.com'
            website = 'cnn'
            title = "Test Article Title"
            content = "This is the content of the test article\nHappy Hanuka!\t\tThis is another line :-)!!!%%%\n*"
            publishing_time = datetime.now()
            collecting_time = datetime.now()
            test_article = Article(
                article_id=article_id, url=url, website=website, title=title, content=content,
                publishing_time=publishing_time, collecting_time=collecting_time
            )
            return db_utils.insert_one(table_name='articles', data=test_article.convert_to_dict())
        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    def test_insert_many(self):
        try:
            db_utils = get_current_db_driver()
            article_id = "article_test_ids"
            url = 'test_article.com'
            website = 'cnn'
            title = "Test Article Title"
            content = "This is the content of the test article\nHappy Hanuka!\t\tThis is another line :-)!!!%%%\n*"
            publishing_time = datetime.now()
            collecting_time = datetime.now()
            test_articles = [Article(
                article_id=article_id, url=url, website=website, title=title, content=content,
                publishing_time=publishing_time, collecting_time=collecting_time
            ),
                Article(
                    article_id=article_id, url=url, website=website, title=title, content=content,
                    publishing_time=publishing_time, collecting_time=collecting_time
                ),
                Article(
                    article_id=article_id, url=url, website=website, title=title, content=content,
                    publishing_time=publishing_time, collecting_time=collecting_time
                )
            ]
            return db_utils.insert_many(table_name='articles', data=test_articles.convert_to_dict())
        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    def test_get_one(self):
        try:
            db_utils = get_current_db_driver()
            data_filter = {'article_id': '05504dac-cb0f-410c-bce4-713482a59e42'}
            article_dict = db_utils.get_one(table_name='articles', data_filter=data_filter)
            if not article_dict:
                self.fail()
            article = get_db_object_from_dict(object_dict=article_dict, class_instance=Article)
            print(article)

        except Exception as e:
            print(f"test_insert_one: {e}")
            self.fail()

    def test_get_many(self):
        try:
            db_utils = get_current_db_driver()
            ids = self.test_insert_many()
            data_filter = {'article_id': ids}
            articles_dict = db_utils.get_many(table_name='articles', data_filter=data_filter)
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
            _id = self.test_insert_one()
            data_filter = {'article_id': _id}
            flag = db_utils.delete_one(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    def test_delete_many(self):
        try:
            db_utils = get_current_db_driver()
            ids = self.test_insert_many()
            data_filter = {'article_id': ids}
            flag = db_utils.delete_many(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_many: {e}")
            self.fail()

    def test_exists(self):
        try:
            db_utils = get_current_db_driver()
            _id = self.test_insert_one()
            data_filter = {'article_id': _id}
            flag = db_utils.exists(table_name='articles', data_filter=data_filter)
            if not flag:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    def test_count(self):
        try:
            db_utils = get_current_db_driver()
            _id = self.test_insert_many()
            data_filter = {'article_id': _id}
            flag = db_utils.count(table_name='articles', data_filter=data_filter)
            if flag == 0:
                self.fail()
        except Exception as e:
            print(f"test_delete_one: {e}")
            self.fail()

    def test_update_one(self):
        # TODO: create test for update one
        pass
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
