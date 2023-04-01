# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import os
from logger import get_current_logger, log_function
import transformers
from sentence_transformers import SentenceTransformer
import numpy as np

logger = get_current_logger()

# Load the BERT model

# model = transformers.BertModel.from_pretrained("bert-base-uncased")
#
# # Define the two texts to compare
# text1 = "The world is a beautiful place full of amazing sights and experiences."
# text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
# tokenizer = transformers.BatchEncoding  # TODO: need to verify this
# # Encode the texts as input for the BERT model
# inputs = tokenizer.encode_plus(text1, text2, return_tensors="pt", max_length=128)
#
# # Pass the encoded inputs through the BERT model
# outputs = model(**inputs)
#
# # Calculate the similarity score between the texts
# similarity_score = outputs[0][0][0].item()
#
# # Print the similarity score
# print(f"Similarity score: {similarity_score}")
#

# This code uses the Hugging Face transformers library to load a pre-trained BERT model and calculate the similarity score between the two input texts. The score will be a value between 0 and 1, with higher values indicating that the texts are more similar in terms of their subject matter.

# You can adjust the parameters of the BERT model and the similarity calculation to fine-tune the results to your specific needs. Additionally, you may want to use other NLP techniques, such as keyword extraction or text summarization, to further analyze the texts and determine their similarity.
from db_utils import Article
from db_utils.db_objects.cluster import Cluster
from exceptions import SimilarityNotFoundException


@log_function
def cluster_similarity(cluster: Cluster, new_article: Article) -> float:
    sim_rate = similarity([cluster.article_content, new_article.content])
    if sim_rate > 75:
        avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
        for article in cluster.articles:
            avg_rate = avg_rate + similarity([new_article, article.summary])
        avg_rate = avg_rate / len(cluster.articles)
        if avg_rate > 60:
            # TODO: add logging here
            logger.debug("High similarity with article , checking average")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
    elif sim_rate > 60:
        avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
        for article in cluster.articles:
            avg_rate = avg_rate + similarity([new_article, article.summary])
        avg_rate = avg_rate / len(cluster.articles)
        if avg_rate > 70:
            # TODO: add logging here
            logger.debug("Low similarity with article , checking average")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
    else:
        desc = f"Error Similarity rate {sim_rate}, Similarity not found"
        logger.debug(f"Similarity not found in {cluster.title}")
        raise SimilarityNotFoundException(desc)  # TODO: add exception similarity not found


@log_function
def summarize(article: Article):
    pass


@log_function
def similarity(self, sentences: list[str]):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v1')
    embeddings = model.encode(sentences)
    d = np.dot(embeddings[0], embeddings[1], out=None)
    # inputs = self.tokenizer.encode_plus(text1, text2, return_tensors="pt", max_length=maxlen)
    # outputs = self.model(**inputs)
    # similarity_score = outputs[0][0][0].item()
    # return similarity_score


@log_function
def find_cluster(clusters: list[Cluster], article: Article):
    # USE_CATEGORIAL_CLASSIFICATION = bool(os.getenv(key="USE_CATEGORIAL_CLASSIFICATION", default=False))

    counter = 0  # im adding this counter to check the number of clusters this subjects corresponds to for stats
    max_topic = None
    max_sim = 0
    for cluster in clusters:
        if article.website not in cluster.websites:
            logger.debug(f"checking similarity in cluster {cluster.title}")
            sim_rate = cluster_similarity(cluster, article)
            if sim_rate > max_sim:
                counter = counter + 1
                max_topic = cluster
                max_sim = sim_rate
    if max_sim > 0:
        max_topic.add_article(article)
        logger.debug(f"Adding article to cluster {max_topic.title}")
        # TODO:add logging here
    else:
        newTopic = Cluster(article)  # needed to add here : a constructor
        logger.debug("Could not find cluster, creating new cluster")
        # TODO: push new article cluster into db
    # if counter > 1:
    #     pass
    # add an error log here to check why it corresponds to more than 1 topic
