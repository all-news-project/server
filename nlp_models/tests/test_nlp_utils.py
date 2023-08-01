import unittest
import itertools

from server_utils.db_utils.general_utils import get_cartesian_product, get_permutations
from nlp_models.model_nlp.model_nlp import NlpModel
from nlp_models.nlp_utils.nlp_utils import NlpUtils
from server_utils.db_driver import get_current_db_driver, DBConsts
from server_utils.db_driver.db_objects.article import Article
from server_utils.db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.logger import log_function, get_current_logger


class MyTestCase(unittest.TestCase):

    def test_prison_not_similar(self):
        artutils = ArticleUtils()
        nlp_utils = NlpUtils()
        art_ids = [["01c15308-ff62-4d57-b8b3-f04ebc890928"], ["d9a08f9d-58a8-40d0-92b3-cfbdf7828d31"]]
        article_texts = []
        for sub in art_ids:
            for _id in sub:
                article_texts.append(artutils.get_article_by_id(_id).content)
        res = nlp_utils.compare_texts(article_texts[0], article_texts[1]) > 0
        print(res)
        self.assertFalse(res)

    @log_function
    def test_syria(self):
        _db = get_current_db_driver()
        logger = get_current_logger()
        nlp = NlpUtils()
        articles_id = ["f9874b36-eed7-4e5d-80fd-d309899cca45", "2fdd46ec-da88-4a72-aa3d-33c152d0b638"]
        articles_dict = []
        for articles_id in articles_id:
            articles_dict.append(
                _db.get_one(table_name=DBConsts.ARTICLES_TABLE_NAME, data_filter={"article_id": articles_id}))
        articles = [get_db_object_from_dict(article, Article) for article in articles_dict]
        bbc = articles[0]
        nbc = articles[1]
        sim = nlp.compare_texts(nbc.content,
                                bbc.content)
        self.assertTrue(sim > 50)

    def test_update_config(self):
        nlp = NlpModel()
        nlp.fit([1, 2], 1)

    def test_summary(self):
        ids = ["d353fe91-5bb9-496c-9164-e57ae0cd457a", "8a0f136d-4eab-4b36-9196-8eeb732381c1",
               "91f5e04d-0489-4bbb-9f80-3219cdbd5e4b"]
        _db = get_current_db_driver()
        data_filter={"article_id": {"$in": ids}}
        articles = _db.get_many(table_name=DBConsts.ARTICLES_TABLE_NAME, data_filter=data_filter)
        article_texts=[]
        for article in articles:
            article_obj=get_db_object_from_dict(article, Article)
            article_texts.append(article_obj.content)
        nlp = NlpUtils()
        #sum=nlp.summarize(article_texts[0])
        sum2=nlp.summarize_text(article_texts[0])
        #sum = nlp.summarize(article.content)
        print(sum)

    def test_syria_russia(self):
        _db = get_current_db_driver()
        logger = get_current_logger()
        nlp = NlpUtils()
        articles_id = ["f9874b36-eed7-4e5d-80fd-d309899cca45", "0810f002-8645-4e76-a001-d6279df3a73d"]
        articles_dict = []
        for articles_id in articles_id:
            articles_dict.append(
                _db.get_one(table_name=DBConsts.ARTICLES_TABLE_NAME, data_filter={"article_id": articles_id}))
        articles = [get_db_object_from_dict(article, Article) for article in articles_dict]
        bbc = articles[0]
        nbc = articles[1]
        sim = nlp.compare_texts(nbc.content, bbc.content)
        self.assertTrue(sim > 50)

    def test_compare_text(self):
        nlp = NlpUtils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.compare_texts(text1, text2)
        self.assertTrue(similarity > 50)

    def test_compare_text_sim(self):
        nlp = NlpUtils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.compare_texts(text1, text2)
        self.assertTrue(similarity > 50)

    def test_not_similar_sim(self):
        nlp = NlpUtils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = nlp.compare_texts(text1, text2)
        self.assertTrue(similarity < 50)


if __name__ == '__main__':
    unittest.main()
