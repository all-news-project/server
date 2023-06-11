import unittest
import itertools

import keras
import numpy as np

from db_driver import get_current_db_driver
from db_driver.db_objects.article import Article
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
from logger import log_function, get_current_logger
from nlp_models.nlp_utils.nlp_utils import Nlp_Utils
from nlp_models.tests.step_test import compare_similarity, compare_texts_tf
from server_utils.db_utils.article_utils import ArticleUtils
import pandas as pd


class MyTestCase(unittest.TestCase):
    similar_articles_ids = [["31c59d24-cca4-4881-8ff6-8da5581c6430", "70239eab-66bb-47c4-8317-ec150dc54fab",
                             "ed99508c-ae5c-4923-b372-dfcb60771ca9"],
                            # us-debt
                            ["a610b426-1555-4534-b487-0395016714f1", "660ac42a-48a8-4e99-8efe-245b37f6777d"],
                            # moscow drone attack
                            ["d353fe91-5bb9-496c-9164-e57ae0cd457a", "8a0f136d-4eab-4b36-9196-8eeb732381c1",
                             "91f5e04d-0489-4bbb-9f80-3219cdbd5e4b"],  # spy satallite
                            ["d9a08f9d-58a8-40d0-92b3-cfbdf7828d31", "9a09712b-6495-4381-9f07-5b2940ef95b0"],
                            # india official
                            ["0fb4c713-6d23-4b96-9213-a84473d365c4", "d9c22f58-74a8-4d1d-8d69-929c60e2904c"],
                            # syria
                            ["d0ca27f5-2bb7-4724-8d85-1950d8322494"]]  # zelensky

    @staticmethod
    def get_permutations(input_dict: dict) -> dict[list[tuple]]:
        """
        input: {"a": [1,2,3], "b":[11,22,33], "c":[111,222]}
        output: {
            "a": [(1,2),(1,3),(2,3)],
            "b": ...
            "c": [(111, 222)]
        }
        :param input_dict:
        :return:
        """
        output = {}
        for k, v in input_dict.items():
            if len(v) < 2:
                continue
            output[k] = []
            for a, b in itertools.permutations(v, 2):
                if (b, a) in output[k]:
                    continue
                else:
                    output[k].append((a, b))
        return output

    def test_get_permutations(self):
        lst = {"a": [1, 2, 3], "b": [11, 22, 33], "c": [111, 222]}
        assert MyTestCase.get_permutations(lst) == {'a': [(1, 2), (1, 3), (2, 3)], 'b': [(11, 22), (11, 33), (22, 33)],
                                                    'c': [(111, 222)]}

    # pass
    def test_get_cartesian_product(self):
        a = {"a": [1, 2, 3],
             "b": [11, 22, 33],
             "c": [111, 222, 333, 444],
             "d": [1111]}
        print(MyTestCase.get_cartesian_product(a))

    @staticmethod
    def get_cartesian_product(input_dict: dict) -> dict:
        """
        input: {"a": [1,2,3], "b":[11,22,33], "c":[111,222], "d":[1111]}
        output: {
            "a:b":[(1,11),(1,22),(1,33),(2,11)...],
            "a:c": ...,
            "a:d": [(1, 1111), (2, 1111), (3, 1111)],
            "b:c": [(11,111), (11,222), (22,111)]...,
            "b:d": [(11, 1111), (22, 1111), (33, 1111)],
            "c:d": [(111, 1111), (222, 1111)],
        }

        a:b, a:c, a:d, .... b:d
        :param input_dict:
        :return:
        """

        return_dict = {}
        for a, b in itertools.combinations(input_dict.keys(), 2):
            return_dict[f"{a}:{b}"] = list(itertools.product(input_dict[a], input_dict[b]))
        return return_dict

    @staticmethod
    def get_similarity_df(sim_dict: dict) -> pd.DataFrame:
        nlp = Nlp_Utils()
        df = pd.DataFrame(columns=['compare_sim', 'compare_text_tf', 'nlp_sim', 'nlp_compare'])
        for subject_title, subject_list in sim_dict.items():
            avg = {'compare_sim': [], 'compare_text_tf': [], 'nlp_sim': [], 'nlp_compare': []}
            for (article_a, article_b) in subject_list:  # TODO: fix avg finding
                avg['compare_sim'].append(compare_similarity(article_a.content, article_b.content))
                avg['compare_text_tf'].append(compare_texts_tf(article_a.content, article_b.content))
                avg['nlp_sim'].append(nlp.similarity(article_a.content, article_b.content))
                avg['nlp_compare'].append(nlp.compare_text([article_a.content, article_b.content]))
            for key in avg.keys():
                diff = max(avg[key]) - min(avg[key])
                avg[key] = (sum(avg[key]) / len(avg[key]), diff)
            df.loc[subject_title] = avg
        return df

    def test_prison_similarity(self):
        artutils = ArticleUtils()
        nlp_utils = Nlp_Utils()
        art_ids = ["01c15308-ff62-4d57-b8b3-f04ebc890928", "01732e2a-fddc-42f4-883e-34d9848bae65",
                   "0c2612c3-5a64-4ada-9c80-83c5088e044b"]
        article_texts = [artutils.get_article_by_id(ids).content for ids in art_ids]
        texts = Nlp_Utils._get_permutations([article_texts])
        for data in texts:
            res=nlp_utils.check_text_similarity(data[0], data[1]) > 0
            print(res)
            assert res>0

    def test_get_model(self):
        nlp = Nlp_Utils()
        nlp.create_model()

    def test_similarity(self):
        nlp = Nlp_Utils()
        nlp.check_similarity()
    def test_prison_not_similar(self):
        artutils = ArticleUtils()
        nlp_utils = Nlp_Utils()
        art_ids = [["01c15308-ff62-4d57-b8b3-f04ebc890928"], ["d9a08f9d-58a8-40d0-92b3-cfbdf7828d31"]]
        article_texts=[]
        for sub in art_ids:
            for _id in sub:
                article_texts.append(artutils.get_article_by_id(_id).content)
        res=nlp_utils.check_text_similarity(article_texts[0], article_texts[1]) > 0
        print(res)
        assert not res
    def test_similar(self):
        logger = get_current_logger()
        artutils = ArticleUtils()
        req_dict = {}
        for subject in self.similar_articles_ids:
            subject_list = []
            for article_id in subject:
                subject_list.append(
                    artutils.get_article_by_id(article_id))
            subject_title = subject_list[0].title
            req_dict[subject_title] = subject_list
        sim_dict = MyTestCase.get_permutations(req_dict)
        df = MyTestCase.get_similarity_df(sim_dict)
        df.to_csv("comparison_results.csv")
        print(df)

    def test_not_similar(self):
        artutils = ArticleUtils()
        logger = get_current_logger()
        nlp = Nlp_Utils()
        req_dict = {}
        for subject in self.similar_articles_ids:
            subject_list = []
            for article_id in subject:
                subject_list.append(
                    artutils.get_article_by_id(article_id))
            subject_title = subject_list[0].title
            req_dict[subject_title] = subject_list
        non_sim_dict = MyTestCase.get_cartesian_product(req_dict)
        df = MyTestCase.get_similarity_df(non_sim_dict)
        df.to_csv("comparison_results.csv")
        print(df)

    def test_product(self):
        a = [[1, 2, 3, 4],
             [11, 22, 33, 44],
             [111, 222, 333, 444],
             [1111]]
        n = list(list(a) for a in itertools.product(*a))
        d = []
        for k in n:
            d.append(list(itertools.combinations(k, 2)))
        k = 5

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
        # sim = nlp.similarity(nbc.content, bbc.content) 0.94
        # sim = nlp.compare_text([nbc.content, bbc.content]) #0.38
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
