import unittest
from nlp_models.nlp_utils import nlp_similizer
import numpy as np
from sentence_transformers import SentenceTransformer

class MyTestCase(unittest.TestCase):
    def test_similarity(self):
        # self.assertEqual(True, False)  # add assertion here
        model = nlp_similizer()
        text1 = "The world is a beautiful place full of amazing sights and experiences."
        text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
        similarity = model.similarity([text1,text2])
        assert similarity>50
    # def test_similar(self):
    #     sentences = ["The world is a beautiful place full of amazing sights and experiences.", "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."]
    #     model = SentenceTransformer('sentence-transformers/all-mpnet-base-v1')
    #     embeddings = model.encode(sentences)
    #     d=np.dot(embeddings[0], embeddings[1], out=None)
    #     print(d)

if __name__ == '__main__':
    unittest.main()
