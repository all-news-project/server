import unittest
from nlp_models.model_two import genis


class MyTestCase(unittest.TestCase):
    def test_similar(self):
        # self.assertEqual(True, False)  # add assertion here
        model = genis()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = model.compare_texts(text1, text2)
        assert similarity

    def test_not_similar(self):
        model = genis()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "The quick red fox jumps over the lazy cat."
        similarity = model.compare_texts(text1, text2)
        assert not similarity


if __name__ == '__main__':
    unittest.main()
