import random
from typing import List

from selenium.webdriver.common.by import By

from db_driver import get_current_db_driver
from logger import log_function, get_current_logger
from scrapers.google_scraper.utils.consts import GoogleScraperConsts
from scrapers.google_scraper.utils.xpaths import TrendXPaths
from scrapers.web_scraper.scraper_drivers import get_scraping_driver


class TrendUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self._driver = get_scraping_driver(via_request=True)

    @staticmethod
    def __clear_trend_text(text: str) -> str:
        if "(" in text:
            text = text.split("(")[0]
        text = text.replace(".", "")
        text = text.replace("&", "and")
        text = text.strip()
        return text

    @staticmethod
    def __is_trend_text_valid(text: str) -> bool:
        if text.isnumeric():
            return False
        return True

    @log_function
    def get_popular_trends(self, shuffle: bool = True) -> List[str]:
        trends: List[str] = []
        self._driver.get_url(GoogleScraperConsts.TREND_WEBSITE_URL)
        elements = self._driver.find_elements(by=By.XPATH, value=TrendXPaths.trends_link)
        for element in elements:
            text: str = self.__clear_trend_text(element.text)
            if self.__is_trend_text_valid(text=text):
                trends.append(text)

        if shuffle:
            random.shuffle(trends)

        self.logger.info(f"Collected {len(trends)} trends")
        return trends
