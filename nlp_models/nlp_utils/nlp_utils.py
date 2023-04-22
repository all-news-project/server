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
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
# from db_utils.db_objects.db_objects_utils import update_cluster, create_new_cluster

import numpy as np

# logger = get_current_logger()


"""This function uses the T5-large model in order to summarize our articles"""


@log_function
def summarize_text(content: str)-> str:
    logger = get_current_logger()
    try:
        model = T5ForConditionalGeneration.from_pretrained('t5-large')  # can change to t5-small
        tokenizer = T5Tokenizer.from_pretrained('t5-large')  # same here
        content = content.strip().replace("\n", "")
        summary = __text_sum(content, model, tokenizer)
        logger.debug("Successfully summarized text")
    except Exception as e:
        logger.error("Failed to summarize text")
        print(e)
        summary = None
    return summary


"""This function uses the sentence transformer to caculate the similarity between 2 texts"""


@log_function
def compare_text(sentences: list[str]) -> float:
    logger = get_current_logger()
    try:
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v1')
        embeddings = model.encode(sentences)
        d = np.dot(embeddings[0], embeddings[1], out=None)
        logger.debug("Similarity rate successful")
        return d
    except Exception as e:
        logger.error("Failed to compare text")
        print(e)
        return 0


""""This function uses the T5 model and tokenizer inorder to encode and decode the text
to get the most important features and summarize the text"""


def __text_sum(text: str, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, num_beams: int = 4,
               no_repeat_ngram_size: int = 2, min_length: int = 30,
               max_length: int = 100,
               early_stopping: bool = True) -> str:
    logger = get_current_logger()
    try:
        t5_prepared_text = "summarize: " + text
        tokenized_text = tokenizer.encode(t5_prepared_text, return_tensors="pt")
        summary_ids = model.generate(tokenized_text,
                                     num_beams=num_beams,
                                     no_repeat_ngram_size=no_repeat_ngram_size,
                                     min_length=min_length,
                                     max_length=max_length,
                                     early_stopping=early_stopping)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        logger.debug("Successfully summarized text")
        return summary
    except Exception as e:
        print(e)
        logger.error("Failed to summarize text")
        return text


# need to look further into transformers

def sim(text_1: str, text_2: str) -> float:
    nlp = spacy.load("en_core_web_lg")
    final_1 = _preprocess(text_1, nlp)
    final_2 = _preprocess(text_2, nlp)
    similarity = final_1.similarity(final_2)
    return similarity


def _preprocess(text, nlp):
    logger = get_current_logger()
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
    return final
