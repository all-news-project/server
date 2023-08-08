from typing import List

from nlp_models.model_nlp.model_nlp import NlpModel
from transformers import AutoTokenizer, LEDConfig, LEDForConditionalGeneration
import numpy as np

from logger import log_function, get_current_logger


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

    def summarize_PRIMERA(self, content: str) -> str:
        tokenizer = AutoTokenizer.from_pretrained('allenai/PRIMERA')
        config = LEDConfig.from_pretrained('allenai/PRIMERA')
        model = LEDForConditionalGeneration.from_pretrained('allenai/PRIMERA')
        input_tokens = tokenizer.encode(content, return_tensors='pt')
        summary_ids = model.generate(input_tokens, max_length=100, num_beams=8, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    @log_function
    def summarize_text(self, content: str) -> str:
        try:
            summary = self.nlp_model.summarize_text(content)
        except Exception as e:
            self.logger.error(f"Failed to summarize text- {e}")
            summary = None
        return summary

    @log_function
    def compare_texts(self, text1, text2):
        sim_rates = self.nlp_model.get_sim(text1, text2)
        reshaped_value = np.array(sim_rates).reshape(1, 2)
        res = self.nlp_model.predict(reshaped_value)
        return res
