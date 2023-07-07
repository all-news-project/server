import os
import time
from typing import List

from tensorflow import keras
import nltk
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from db_driver import get_current_db_driver
from logger import get_current_logger, log_function
from nlp_models.nlp_utils.consts import NlpConsts
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.db_utils.general_utils import get_cartesian_product, get_permutations

from transformers import T5Tokenizer, T5ForConditionalGeneration, DistilBertTokenizer, DistilBertModel

from sentence_transformers import SentenceTransformer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


class NlpModel:
    MODELS_FILE_PATH = os.getenv(key="MODELS_FILE_PATH", default="./model_files")

    def __init__(self):
        # t=Functional()
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        self._db = get_current_db_driver()
        self._similar_inputs = 0
        self._non_similar_inputs = 0
        self.logger = get_current_logger()
        self._model_path=(os.path.join(self.MODELS_FILE_PATH, "model_nlp.h5"))
        self._model = keras.models.load_model(self._model_path)

    def _create_model(self):
        import random
        texts = self._get_articles_texts(NlpConsts.TRAINING_ARTICLES_ID)
        similar_texts = get_permutations(texts)
        non_similar_texts = get_cartesian_product(texts)
        non_similar_texts = random.sample(non_similar_texts, self._non_similar_inputs)
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
        model = keras.models.Sequential([
            keras.layers.Input(shape=2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(x_data, y_data, epochs=10)
        model.save(self._model_path)

    @staticmethod
    def _get_articles_texts(ids_list: list):
        """This function uses the T5-large model_nlp in order to summarize our articles"""
        articles_utils = ArticleUtils()
        articles_text = []
        for subject in ids_list:
            subject_list = []
            for article_id in subject:
                subject_list.append(
                    articles_utils.get_article_by_id(article_id).content)
            articles_text.append(subject_list)
        return articles_text

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

    @log_function
    def _nltk_similarity(self, text1, text2):
        # nltk.download('stopwords')
        # nltk.download('punkt')
        # nltk.download('wordnet')
        # Preprocess the texts
        preprocessed_text1 = self._preprocess_text(text1)
        preprocessed_text2 = self._preprocess_text(text2)
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])
        # Compute cosine similarity
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity * 100

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

    @log_function
    def _transformers_similarity(self, sentences: list[str]) -> float:
        """
        This function uses the sentence transformer to calculate the similarity between 2 texts
        """
        try:
            model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
            embeddings = model.encode(sentences)
            d = np.dot(embeddings[0], embeddings[1], out=None)
            return d * 100
        except Exception as e:
            self.logger.error("Failed to compare text")
            print(e)
            return 0

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

    """"This function uses the T5 model_nlp and tokenizer inorder to encode and decode the text
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

    @log_function
    def categorize(self, content: str):
        """This function uses the DistilBert pretrained model_nlp by valurank in order to categorize articles."""
        tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
        model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
        encoded_input = tokenizer.encode(content, return_tensors='pt')
        output = model(**encoded_input)
        return output

    def get_sim(self, text1, text2):
        nltk_sim = self._nltk_similarity(text1, text2)
        trans_sim = self._transformers_similarity([text1, text2])
        return [nltk_sim, trans_sim]

    # todo: @Tal implement fit & save - using self.model_nlp.fit
    def fit(self, rates: List[float], label: int):
        self._model.fit(rates, label)
        if label==1:
            self._db.update_one(table_name="models_config",data_filter={"name":"similar_inputs"},new_data={"num":self._similar_inputs+1})
        elif label == 0:
            self._db.update_one(table_name="models_config", data_filter={"name": "non_similar_inputs"},
                                new_data={"num": self._non_similar_inputs + 1})
        self._model.save(self._model_path)

    def predict(self, rates: List[float]):
        self._get_model_config()
        res = self._model.predict(rates)[0][0]
        if res > 0.90 and abs(
                self._similar_inputs - self._non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
            self.fit(rates, 1)
            # self.nlp_model.save("model_nlp.h5")
        elif res < 0.15 and abs(
                self._similar_inputs - self._non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
            self.fit(rates, 0)
        return res
    def _get_model_config(self):
        self._similar_inputs = self._db.get_one(table_name="models_config", data_filter={'name': 'similar_inputs'})[
            'num']
        self._non_similar_inputs = \
        self._db.get_one(table_name="models_config", data_filter={'name': 'non_similar_inputs'})['num']
    # def check_similarity(self):
    #     artutils = ArticleUtils()
    #     model_nlp = keras.model_nlp.load_model("model_nlp.h5")
    #     art_ids = ["01c15308-ff62-4d57-b8b3-f04ebc890928", "01732e2a-fddc-42f4-883e-34d9848bae65",
    #                "0c2612c3-5a64-4ada-9c80-83c5088e044b"]
    #     article_texts = [artutils.get_article_by_id(ids).content for ids in art_ids]
    #     texts = self._get_permutations([article_texts])
    #     x_data, y_data = self._get_similarity_data(texts, 1)
    #     res = []
    #     for data in x_data:
    #         reshaped_value = np.array(data).reshape(1, 2)
    #         res.append(int(model_nlp.predict(reshaped_value)))
