# To check if two texts are written about the same subject using natural language processing (NLP) techniques,
# you can first extract the main topics or themes from each text using a topic modeling algorithm. Then,
# you can compare the resulting topics and see if there is any overlap between them.

# Here is an example of how you might use the Gensim library to extract the topics from two texts and compare them:

# Copy code
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

# Define the two texts to compare
# text1 = "The quick brown fox jumps over the lazy dog."
# text2 = "The quick red fox jumps over the lazy cat."


#
# # Pre-process the texts to remove stopwords and stem the words
# stemmer = SnowballStemmer("english")
#
#
# def preprocess(text):
#     result = []
#     for token in gensim.utils.simple_preprocess(text):
#         if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
#             result.append(stemmer.stem(token))
#     return result
#
#
# processed_text1 = preprocess(text1)
# processed_text2 = preprocess(text2)
#
# # Use the LDA model to extract the topics from the texts
# dictionary = gensim.corpora.Dictionary([processed_text1, processed_text2])
# corpus = [dictionary.doc2bow(text) for text in [processed_text1, processed_text2]]
# lda_model = gensim.models.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=10)
#
# # Print the extracted topics
# for idx, topic in lda_model.print_topics(-1):
#     print(f"Topic: {idx} \nWords: {topic}")
#
# # Check if the topics from the two texts overlap
# topics1 = set([word for word, _ in lda_model.get_topic_terms(0, topn=10)])
# topics2 = set([word for word, _ in lda_model.get_topic_terms(1, topn=10)])
# common_topics = topics1.intersection(topics2)
# if common_topics:
#     print(f"The texts are about the same subject: {common_topics}")
# else:
#     print("The texts are not about the same subject.")
#

# This code uses the Gensim library to apply the Latent Dirichlet Allocation (LDA) algorithm to the two texts, and then extracts the top 10 words from each topic. It then compares the resulting topics to see if there is any overlap, and prints a message indicating whether the texts are about the same subject or not.

# Note that this code is just an example, and you may need to adjust the parameters and settings of the LDA model to get the best results for your specific texts. Additionally, you may want to use other topic modeling algorithms or NLP techniques to extract the topics from the texts.

class genis:
    def __init__(self, stemmer=SnowballStemmer("english")):
        self.stemmer = stemmer

    def compare_texts(self, text1, text2):
        processed_text1 = self._preprocess(text1)
        processed_text2 = self._preprocess(text2)
        dictionary = gensim.corpora.Dictionary([processed_text1, processed_text2])
        corpus = [dictionary.doc2bow(text) for text in [processed_text1, processed_text2]]
        lda_model = gensim.models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)
        topics1 = set([word for word, _ in lda_model.get_topic_terms(0, topn=10)])
        topics2 = set([word for word, _ in lda_model.get_topic_terms(1, topn=10)])
        common_topics = topics1.intersection(topics2)
        return common_topics

    def _preprocess(self, text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(self.stemmer.stem(token))
        return result
