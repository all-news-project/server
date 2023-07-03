from typing import List

from logger import get_current_logger, log_function
from nlp_models.models.nlp_model import NlpModel
from nlp_models.nlp_utils.consts import NlpConsts
import numpy as np


class NlpUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self.nlp_model = NlpModel()

    @log_function
    def categorize_article(self, article_content: str) -> List[str]:
        try:
            self.logger.debug("Categorizing article")
            category = self.nlp_model.categorize(article_content)
            self.logger.info(f"Categorized article to `{category}`")
            return category
        except Exception as e:
            self.logger.error(f"Failed categorize article")
            raise e

    @log_function
    def summarize_text(self, content: str) -> str:
        try:
            summary = self.nlp_model.summarize_text(content)
            self.logger.debug("Successfully summarized text")
        except Exception as e:
            self.logger.error("Failed to summarize text")
            print(e)
            summary = None
        return summary

    @log_function
    def compare_texts(self, text1, text2):
        sim_rates = self.nlp_model.get_sim(text1, text2)
        reshaped_value = np.array(sim_rates).reshape(1, 2)
        res = self.nlp_model.predict(reshaped_value)
        # if res > 0.90 and abs(
        #         self.nlp_model.similar_inputs - self.nlp_model.non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
        #     self.nlp_model.fit(sim_rates, 1)
        #     # self.nlp_model.save("models.h5")
        # elif res < 0.15 and abs(
        #         self.nlp_model.similar_inputs - self.nlp_model.non_similar_inputs) < NlpConsts.DIFFERENCE_LABEL_TOLERANCE:
        #     self.nlp_model.fit(sim_rates, 0)
            # self.nlp_model.save("models.h5")
        return res  # > 0.65
