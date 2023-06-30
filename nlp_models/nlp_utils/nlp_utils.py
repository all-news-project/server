# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import itertools
import time

import nltk
import pandas as pd
import keras
import spacy
from nltk import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

from keras import layers
from nltk.corpus import stopwords

from logger import get_current_logger, log_function
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_models.nlp_utils.consts import NlpConsts
import numpy as np

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
        self.similar_inputs = 9
        self.non_similar_inputs = 9
        self.logger = get_current_logger()
        self.model = keras.models.load_model("nlp_model.h5")

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

    def _get_similarity_data(self, data_list: list, label: int):
        x_data = []
        i = 0
        for a, b in data_list:
            print(f'iteration {i} - {len(data_list) - i} left')
            i = i + 1
            avg = [self._nltk_similarity(a, b), self._transformers_similarity([a, b])]
            x_data.append(avg)
        if label == 1:
            label_list = np.ones(shape=len(x_data))
        else:
            label_list = np.zeros(shape=len(x_data))
        return x_data, list(label_list)
    def _get_sim(self,text1,text2):
        nltk_sim=self._nltk_similarity(text1, text2)
        trans_sim=self._transformers_similarity([text1,text2])
        return [nltk_sim,trans_sim]
    def check_runtime_similarity(self, text1, text2):
        with open("runtimes.txt", "w") as f:
            start = time.time()
            f_model = self._nltk_similarity(text1, text2)
            end = time.time()
            f.write(f"compare similarity- {end - start}\n")
            start = time.time()
            t_model = self._transformers_similarity([text1, text2])
            end = time.time()
            f.write(f"compare text- {end - start}\n")
            sim_rates = [f_model, t_model]
            f.close()
            return sim_rates  # > 0.65

    def check_similarity(self):
        artutils = ArticleUtils()
        model = keras.models.load_model("nlp_model.h5")
        art_ids = ["01c15308-ff62-4d57-b8b3-f04ebc890928", "01732e2a-fddc-42f4-883e-34d9848bae65",
                   "0c2612c3-5a64-4ada-9c80-83c5088e044b"]
        article_texts = [artutils.get_article_by_id(ids).content for ids in art_ids]
        texts = self._get_permutations([article_texts])
        x_data, y_data = self._get_similarity_data(texts, 1)
        res = []
        for data in x_data:
            reshaped_value = np.array(data).reshape(1, 2)
            res.append(int(model.predict(reshaped_value)))

    def create_model(self):
        import random
        texts = _get_articles_texts(NlpConsts.TRAINING_ARTICLES_ID)
        similar_texts = self._get_permutations(texts)
        non_similar_texts = self._get_cartesian_product(texts)
        non_similar_texts = random.sample(non_similar_texts, self.non_similar_inputs)
        x_sim, y_sim = self._get_similarity_data(similar_texts, 1)
        x_non_sim, y_non_sim = self._get_similarity_data(non_similar_texts, 0)
        x_data = x_sim + x_non_sim
        y_data = y_sim + y_non_sim
        df = pd.DataFrame({'model_1': [m1[0] for m1 in x_data], 'model_2': [m2[1] for m2 in x_data], 'label': y_data})
        sim_data = df[df['label'] == 1]
        non_sim_data = df[df['label'] == 0]
        new_df = pd.concat([sim_data, non_sim_data])
        new_df.reset_index(drop=True, inplace=True)
        df = new_df.sample(frac=1).reset_index(drop=True)
        x_data = df.drop(columns='label')  # ['data']
        y_data = df['label']
        model = keras.Sequential([
            keras.layers.Input(shape=(2)),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(x_data, y_data, epochs=10)
        model.save("nlp_model.h5")

    @log_function
    def _nltk_similarity(self, text1, text2):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        # Preprocess the texts
        preprocessed_text1 = self._preprocess_text(text1)
        preprocessed_text2 = self._preprocess_text(text2)
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])
        # Compute cosine similarity
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity*100

    def _preprocess_text(self, text):
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [token for token in tokens if token not in stop_words]
        # Lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        # Join the tokens back into a single string
        preprocessed_text = " ".join(lemmatized_tokens)
        return preprocessed_text

    """This function uses the sentence transformer to calculate the similarity between 2 texts"""

    @log_function
    def _transformers_similarity(self, sentences: list[str]) -> float:
        try:
            model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
            embeddings = model.encode(sentences)
            d = np.dot(embeddings[0], embeddings[1], out=None)
            return d * 100
        except Exception as e:
            self.logger.error("Failed to compare text")
            print(e)
            return 0

    def compare_texts(self, text1, text2):
        sim_rates = self.get_sim(text1, text2)
        reshaped_value = np.array(sim_rates).reshape(1, 2)
        res = self.model.predict(reshaped_value)[0][0]
        if res > 0.90 and abs(
                self.similar_inputs - self.non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
            self.model.fit(sim_rates, 1)
            self.model.save("nlp_model.h5")
        elif res < 0.15 and abs(
                self.similar_inputs - self.non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
            self.model.fit(sim_rates, 0)
            self.model.save("nlp_model.h5")
        return res #> 0.65
