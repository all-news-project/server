# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import os

import db_utils
from logger import get_current_logger, log_function
import transformers
from transformers import DistilBertModel, DistilBertTokenizer, T5Tokenizer, T5ForConditionalGeneration, BertModel, \
    BertTokenizer
from sentence_transformers import SentenceTransformer
from db_utils.db_objects.db_objects_utils import update_cluster, create_new_cluster
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

db = db_utils.get_current_db_driver()
"""This function is used to check the similarity between unclassified article and a specific cluster's articles"""


@log_function
def cluster_similarity(cluster: Cluster, new_article: Article) -> float:
    sim_rate = compare_text([cluster.article_content, new_article.content])

    if sim_rate > 60:
        avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
        articles = db.get_many("articles", {"article_id": cluster.articles_id})
        for article in articles:
            avg_rate = avg_rate + compare_text([new_article, article.summary])
        avg_rate = avg_rate / len(articles)
        if sim_rate > 75 and avg_rate >60:
            logger.debug(f"High similarity with article,average{avg_rate}")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
        elif sim_rate >60 and avg_rate >70:
            logger.debug(f"Low similarity with article,average{avg_rate}")
            # self.add_article(newArticle)
            return (avg_rate + sim_rate) / 2
    # elif sim_rate > 60:
    #     avg_rate = 0  # this look better , but its easier to understand the bottom ->sum([self.similizer.similarity([newArticle])])
    #     for article in cluster.articles:
    #         avg_rate = avg_rate + compare_text([new_article, article.summary])
    #     avg_rate = avg_rate / len(cluster.articles)
    #     if avg_rate > 70:
    #         logger.debug("Low similarity with article , checking average")
    #         # self.add_article(newArticle)
    #         return (avg_rate + sim_rate) / 2
    else:
        desc = f"Error Similarity rate {sim_rate}, Similarity not found"
        logger.debug(f"Similarity not found in {cluster.title}")
        raise SimilarityNotFoundException(desc)  # TODO: add exception similarity not found


"""This function uses the T5-large model in order to summarize our articles"""


@log_function
def summarize_text(content: str):
    # articles = data['Text'].tolist()
    model = T5ForConditionalGeneration.from_pretrained('t5-large')  # can change to t5-small
    tokenizer = T5Tokenizer.from_pretrained('t5-large')  # same here
    content = content.strip().replace("\n", "")
    return __article_sum(content, model, tokenizer)


"""This function uses the sentence transformer to caculate the similarity between 2 texts"""


@log_function
def compare_text(sentences: list[str]):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v1')
    embeddings = model.encode(sentences)
    d = np.dot(embeddings[0], embeddings[1], out=None)
    # inputs = self.tokenizer.encode_plus(text1, text2, return_tensors="pt", max_length=maxlen)
    # outputs = self.model(**inputs)
    # similarity_score = outputs[0][0][0].item()
    # return similarity_score


"""This function searches every cluster in the database to find the best match for the current article
    by checking the similarity rate of every article in each cluster"""


@log_function
def classify_article(clusters: list[Cluster], article: Article):
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
        # max_topic.articles_id.append(article.article_id)
        update_cluster(max_topic, article)
        # max_topic.add_article(article)
        logger.debug(f"Adding article to cluster {max_topic.title}")
    else:
        create_new_cluster(article)
        logger.debug("Could not find cluster, creating new cluster")
    # if counter > 1:
    #     pass
    # add an error log here to check why it corresponds to more than 1 topic


"""This function uses the DistilBert pretrained model by valurank in order to categorize articles."""


@log_function
def categorize_article(article: Article):
    logger.debug("Categorizing article")
    tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
    model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
    encoded_input = tokenizer.encode(article.content, return_tensors='pt')
    output = model(**encoded_input)
    return output


""""This function uses the T5 model and tokenizer inorder to encode and decode the text
to get the most important features and summarize the text"""


def __article_sum(article, model, tokenizer: T5Tokenizer):
    t5_prepared_text = "summarize: " + article
    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt")
    summary_ids = model.generate(tokenized_text,
                                 num_beams=4,
                                 no_repeat_ngram_size=2,
                                 min_length=30,
                                 max_length=100,
                                 early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
