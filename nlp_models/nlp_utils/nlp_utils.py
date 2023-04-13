# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import datetime
import os
import uuid

import spacy
from nltk import PorterStemmer

import db_utils
from logger import get_current_logger, log_function
import transformers
from transformers import DistilBertModel, DistilBertTokenizer, T5Tokenizer, T5ForConditionalGeneration, BertModel, \
    BertTokenizer
from sentence_transformers import SentenceTransformer
from nltk.tokenize import  sent_tokenize,word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
# from db_utils.db_objects.db_objects_utils import update_cluster, create_new_cluster

import numpy as np

logger = get_current_logger()


# This code uses the Hugging Face transformers library to load a pre-trained BERT model and calculate the similarity score between the two input texts. The score will be a value between 0 and 1, with higher values indicating that the texts are more similar in terms of their subject matter.

# You can adjust the parameters of the BERT model and the similarity calculation to fine-tune the results to your specific needs. Additionally, you may want to use other NLP techniques, such as keyword extraction or text summarization, to further analyze the texts and determine their similarity.



"""This function uses the T5-large model in order to summarize our articles"""


@log_function
def summarize_text(content: str):
    # articles = data['Text'].tolist()
    model = T5ForConditionalGeneration.from_pretrained('t5-large')  # can change to t5-small
    tokenizer = T5Tokenizer.from_pretrained('t5-large')  # same here
    content = content.strip().replace("\n", "")
    return __text_sum(content, model, tokenizer)


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


""""This function uses the T5 model and tokenizer inorder to encode and decode the text
to get the most important features and summarize the text"""


def __text_sum(text: str, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, num_beams: int = 4,
               no_repeat_ngram_size: int = 2, min_length: int = 30,
               max_length: int = 100,
               early_stopping: bool = True) -> str:
    t5_prepared_text = "summarize: " + text
    tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt")
    summary_ids = model.generate(tokenized_text,
                                 num_beams=num_beams,
                                 no_repeat_ngram_size=no_repeat_ngram_size,
                                 min_length=min_length,
                                 max_length=max_length,
                                 early_stopping=early_stopping)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# need to look further into transformers

def sim(text1, text2):
    nlp = spacy.load("en_core_web_lg")
    final_1 = _preprocess(text1, nlp)
    final_2 = _preprocess(text2, nlp)
    similarity = final_1.similarity(final_2)

def _preprocess(text, nlp):
    result_1 = []
    logger.debug("Preprocessing Text")
    process1 = nlp(text.lower())
    # This is the lemmatization process
    for token in process1:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == "-PRON-":
            continue
        result_1.append(token.lemma_)
    result1 = " ".join(result_1)
    final = nlp(result1)
    #cv = TfidfVectorizer()
    #x=cv.fit_transform(final)#.toarray()
    # stemmer=PorterStemmer()
    return final
