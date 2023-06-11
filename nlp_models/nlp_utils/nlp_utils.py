# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import datetime
import itertools
import os
import random
import uuid
import pandas as pd
import keras
import spacy
from nltk import PorterStemmer
from keras import layers
from logger import get_current_logger, log_function
import transformers
from transformers import DistilBertModel, DistilBertTokenizer, T5Tokenizer, T5ForConditionalGeneration, BertModel, \
    BertTokenizer
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
# from db_utils.db_objects.db_objects_utils import add_article_to_cluster, create_new_cluster
from nlp_models.nlp_utils.consts import NlpConsts
import numpy as np

from nlp_models.tests.step_test import compare_texts_tf, compare_similarity
from server_utils.db_utils.article_utils import ArticleUtils

# logger = get_current_logger()


"""This function uses the T5-large model in order to summarize our articles"""


def _get_articles_texts(ids_list: list):
    artutils = ArticleUtils()
    articles_text = []
    for subject in ids_list:
        subject_list = []
        for article_id in subject:
            subject_list.append(
                artutils.get_article_by_id(article_id).content)
        articles_text.append(subject_list)
    return articles_text


class Nlp_Utils:
    def __init__(self):
        self.logger = get_current_logger()

    @log_function
    def summarize_text(self, content: str) -> str:
        try:
            model = T5ForConditionalGeneration.from_pretrained('t5-large')  # can change to t5-small
            tokenizer = T5Tokenizer.from_pretrained('t5-large')  # same here
            content = content.strip().replace("\n", "")
            summary = self.__text_sum(content, model, tokenizer)
            self.logger.debug("Successfully summarized text")
        except Exception as e:
            self.logger.error("Failed to summarize text")
            print(e)
            summary = None
        return summary

    """This function uses the sentence transformer to calculate the similarity between 2 texts"""

    @log_function
    def compare_text(self, sentences: list[str]) -> float:
        try:
            model = SentenceTransformer('sentence-transformers/all-mpnet-base-v1')
            embeddings = model.encode(sentences)
            d = np.dot(embeddings[0], embeddings[1], out=None)
            # self.logger.debug("Similarity rate successful")
            return d * 100
        except Exception as e:
            self.logger.error("Failed to compare text")
            print(e)
            return 0

    """"This function uses the T5 model and tokenizer inorder to encode and decode the text
    to get the most important features and summarize the text"""

    @log_function
    def __text_sum(self, text: str, model: T5ForConditionalGeneration, tokenizer: T5Tokenizer, num_beams: int = 4,
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
    @log_function
    def similarity(self, text_1: str, text_2: str) -> float:
        nlp = spacy.load("en_core_web_lg")
        final_1 = self._preprocess(text_1, nlp)
        final_2 = self._preprocess(text_2, nlp)
        similarity = final_1.similarity(final_2)
        return similarity

    @log_function
    def _preprocess(self, text, nlp):
        result_1 = []
        self.logger.debug("Preprocessing Text")
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

    @staticmethod
    def _get_permutations(input_list: list) -> list[tuple]:
        """
        input: [[1,2,3],[11,22,33],[111,222]]
        output: [
            (1,2),(1,3),(2,3),
            ...
            ,(111, 222)
        ]
        :param input_list:
        :return:
        """
        output = []
        for v in input_list:
            if len(v) < 2:
                continue
            # output[k] = []
            for a, b in itertools.permutations(v, 2):
                if (b, a) in output:
                    continue
                else:
                    output.append((a, b))
        return output

    @staticmethod
    def _get_cartesian_product(input_list: list) -> list:
        """
        input: [[1,2,3],[11,22,33],[111,222], [1111]]
        output: [
            [(1,11),(1,22),(1,33),(2,11)...],
             ...,
             [(1, 1111), (2, 1111), (3, 1111)],
             [(11,111), (11,222), (22,111)]...,
             [(11, 1111), (22, 1111), (33, 1111)],
             [(111, 1111), (222, 1111)],
        ]

        a:b, a:c, a:d, .... b:d
        :param input_dict:
        :return:
        """

        return_list = []
        for a, b in itertools.combinations(input_list, 2):
            return_list.extend(list(itertools.product(a, b)))
        return return_list

    def get_similarity_data(self, data_list: list, label: int):
        x_data = []
        i = 0
        for a, b in data_list:
            print(f'iteration {i} - {len(data_list) - i} left')
            i = i + 1
            avg = [compare_similarity(a, b), compare_texts_tf(a, b), self.compare_text([a, b])]
            x_data.append(avg)
        if label == 1:
            label_list = np.ones(shape=len(x_data))
        else:
            label_list = np.zeros(shape=len(x_data))
        return x_data, list(label_list)

    def check_text_similarity(self, text1, text2):
        model = keras.models.load_model("nlp_model.h5")
        sim_rates = [compare_similarity(text1, text2), compare_texts_tf(text1, text2),
                     self.compare_text([text1, text2])]
        reshaped_value = np.array(sim_rates).reshape(1, 3)
        res = model.predict(reshaped_value)[0][0]
        return res > 0.65

    def check_similarity(self):
        artutils = ArticleUtils()
        model = keras.models.load_model("nlp_model.h5")
        art_ids = ["01c15308-ff62-4d57-b8b3-f04ebc890928", "01732e2a-fddc-42f4-883e-34d9848bae65",
                   "0c2612c3-5a64-4ada-9c80-83c5088e044b"]
        article_texts = [artutils.get_article_by_id(ids).content for ids in art_ids]
        texts = self._get_permutations([article_texts])
        x_data, y_data = self.get_similarity_data(texts, 1)
        res = []
        for data in x_data:
            reshaped_value = np.array(data).reshape(1, 3)
            res.append(int(model.predict(reshaped_value)))

    def create_model(self):
        texts = _get_articles_texts(NlpConsts.TRAINING_ARTICLES_ID)
        similar_texts = self._get_permutations(texts)
        non_similar_texts = self._get_cartesian_product(texts)
        x_sim, y_sim = self.get_similarity_data(similar_texts, 1)
        x_non_sim, y_non_sim = self.get_similarity_data(non_similar_texts, 0)
        x_data = x_sim + x_non_sim
        y_data = y_sim + y_non_sim
        df = pd.DataFrame({'data': x_data, 'label': y_data})
        # df.to_csv("data_label_df.csv")
        # df = pd.read_csv("data_label_df.csv")
        sim_data = df[df['label'] == 1]
        non_sim_data = df[df['label'] == 0].sample(9)
        new_df = pd.concat([sim_data, non_sim_data])
        new_df.reset_index(drop=True, inplace=True)
        df = new_df.drop(new_df.columns[0], axis=1)
        df = df.sample(frac=1).reset_index(drop=True)
        x_data = df['data']
        y_data = df['label']
        # for data in x_data:
        #    #d = data[1:-1].split(',')
        #    r_data.append(float(data))
        # x_data = r_data
        model = keras.Sequential([
            keras.layers.Input(shape=(3)),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(x_data, y_data, epochs=10)
        model.save("nlp_model.h5")
