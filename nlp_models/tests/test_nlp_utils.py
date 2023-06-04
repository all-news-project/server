import unittest

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
from logger import log_function, get_current_logger
from nlp_models.nlp_utils.nlp_utils import Nlp_Utils
from nlp_models.tests.step_test import compare_similarity, compare_texts_tf


class MyTestCase(unittest.TestCase):
    def test_similar(self):
        pass
    @log_function
    def test_syria(self):
        _db = get_current_db_driver()
        logger = get_current_logger()
        nlp = Nlp_Utils()
        articles_id = ["f9874b36-eed7-4e5d-80fd-d309899cca45", "2fdd46ec-da88-4a72-aa3d-33c152d0b638"]

        articles_dict = []
        for articles_id in articles_id:
            articles_dict.append(
                _db.get_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter={"article_id": articles_id}))
        articles = [get_db_object_from_dict(article, Article) for article in articles_dict]
        bbc = articles[0]
        nbc = articles[1]
        # sim = nlp.similarity(nbc.content, bbc.content) 0.96
        # sim= nlp.compare_text([nbc.content, bbc.content]) #0.68
        # sim=compare_similarity(nbc.content,bbc.content) # 0.40
        sim = compare_texts_tf(nbc.content, bbc.content)  # -0.85 , maybe its reversed?
        assert sim > 50

    def test_syria_russia(self):
        _db = get_current_db_driver()
        logger = get_current_logger()
        nlp = Nlp_Utils()
        articles_id = ["f9874b36-eed7-4e5d-80fd-d309899cca45", "0810f002-8645-4e76-a001-d6279df3a73d"]

        articles_dict = []
        for articles_id in articles_id:
            articles_dict.append(
                _db.get_one(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter={"article_id": articles_id}))
        articles = [get_db_object_from_dict(article, Article) for article in articles_dict]
        bbc = articles[0]
        nbc = articles[1]
        # TODO: sim = nlp.similarity(nbc.content, bbc.content) similarity isn't the best way to check , need to further
        # check to improve it
        # sim = nlp.compare_text([nbc.content, bbc.content]) #0.38
        # sim = nlp.similarity(nbc.content, bbc.content) 0.94
        # sim = compare_similarity(nbc.content, bbc.content)# 0.099
        sim = compare_texts_tf(nbc.content, bbc.content)  # -0.51??
        assert sim < 50
        k = 5
        logger.info("stop")

    def test_compare_text(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.compare_text([text1, text2])
        assert similarity > 50

    def test_not_similar(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = nlp.compare_text([text1, text2])
        assert similarity < 50

    def test_compare_text_sim(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.similarity(text1, text2)
        assert similarity > 50

    def test_not_similar_sim(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = nlp.similarity(text1, text2)
        assert similarity < 50


if __name__ == '__main__':
    unittest.main()
