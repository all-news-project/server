import os
from datetime import datetime
from typing import List

from selenium.webdriver.common.by import By

from db_driver.db_objects.article import Article
from logger import get_current_logger, log_function
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase
from scrapers.scraper_drivers import get_scraping_driver
from scrapers.websites_scrapers.utils.consts import ScraperConsts, MainConsts
from scrapers.websites_scrapers.utils.exceptions import FailedGetURLException


class BBCScraper(WebsiteScraperBase):
    USE_REQUEST_DRIVER = bool(os.getenv(key="USE_REQUEST_DRIVER", default=True))
    HEADLESS = bool(os.getenv(key="HEADLESS", default=True))

    def __init__(self):
        self.logger = get_current_logger()
        self._driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        self._url = ScraperConsts.BBC_HOME_PAGE

    @log_function
    def _get_home_page(self):
        exception = None
        for trie in range(MainConsts.TIMES_TRY_GET_HOMEPAGE):
            try:
                self._driver.get_url(url=self._url)
                self.logger.info(f"Successfully get home page -> `{self._url}`")
                return
            except Exception as e:
                exception = e
                desc = f"Cannot get into home page try NO. {trie + 1}/{MainConsts.TIMES_TRY_GET_HOMEPAGE} - {str(e)}"
                self.logger.warning(desc)
        desc = f"Failed get home page -> {self._url} after {MainConsts.TIMES_TRY_GET_HOMEPAGE} tries - {exception}"
        self.logger.error(desc)
        raise FailedGetURLException(desc)

    def _get_article_page(self, url: str):
        raise NotImplementedError

    def _get_article_title(self) -> str:
        raise NotImplementedError

    def _get_article_content_text(self) -> str:
        raise NotImplementedError

    def _get_article_publishing_time(self) -> datetime:
        raise NotImplementedError

    def _get_article_category(self) -> str:
        # default return - 'general'
        raise NotImplementedError

    def _get_article_image_urls(self) -> List[str]:
        # default return - empty list
        raise NotImplementedError

    def _get_article_state(self) -> str:
        # default return - 'global'
        raise NotImplementedError

    def get_new_article_urls_from_home_page(self) -> List[str]:
        self._get_home_page()
        articles_urls = []
        articles_elements = self._driver.find_elements(by=By.CLASS_NAME, value="block-link__overlay-link")
        for element in articles_elements:
            href = element.get_attribute("href")
            if self._url not in href:
                href = self._url + href
            articles_urls.append(href)
        return articles_urls

    def get_article(self, url: str) -> Article:
        raise NotImplementedError
