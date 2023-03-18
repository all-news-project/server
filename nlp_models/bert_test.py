import unittest
from nlp_models.model_one import Bert


class MyTestCase(unittest.TestCase):
    def test_similarity(self):
        # self.assertEqual(True, False)  # add assertion here
        model = Bert()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = model.similarity(text1, text2, 128)
        assert similarity>50


if __name__ == '__main__':
    unittest.main()
