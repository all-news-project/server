import unittest
from nlp_models.nlp_utils.nlp_utils import Nlp_Utils


class MyTestCase(unittest.TestCase):

    def test_compare_text(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.compare_text([text1, text2])
        assert similarity>50

    def test_not_similar(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = nlp.compare_text([text1, text2])
        assert  similarity<50
    def test_compare_text_sim(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = nlp.similarity(text1, text2)
        assert similarity>50

    def test_not_similar_sim(self):
        nlp = Nlp_Utils()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = nlp.similarity(text1, text2)
        assert  similarity<50




if __name__ == '__main__':
    unittest.main()
