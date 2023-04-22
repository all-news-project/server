import unittest
from nlp_models.nlp_utils.nlp_utils import compare_text


class MyTestCase(unittest.TestCase):
    def test_compare_text(self):
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = compare_text([text1, text2])
        assert similarity>50

    def test_not_similar(self):
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = compare_text([text1, text2])
        assert  similarity<50


if __name__ == '__main__':
    unittest.main()
