import re
from datetime import datetime
from typing import List
from uuid import uuid4

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from db_driver.db_objects.article import Article
from db_driver.db_objects.task import Task
from logger import log_function
from scrapers.websites_scrapers.utils.exceptions import UnwantedArticleException
from scrapers.websites_scrapers.utils.xpaths import BBCXPaths
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase
from scrapers.websites_scrapers.utils.consts import ScraperConsts, MainConsts


class BBCScraper(WebsiteScraperBase):
    def __init__(self):
        super().__init__()
        self._homepage_url = ScraperConsts.BBC_HOME_PAGE

    def _get_article_title(self) -> str:
        return self._driver.get_title()

    def _get_article_content_text(self) -> str:
        text_content = ""
        paragraphs = self._driver.find_elements(by=By.XPATH, value=BBCXPaths.text_block)
        if not paragraphs:
            self.logger.error(f"Error find elements: ")
            return text_content
        else:
            return " ".join([paragraph.get_text() for paragraph in paragraphs])

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

    def _check_unwanted_article(self):
        self.logger.debug(f"_check_unwanted_article, current -> {self._driver.get_current_url()}")
        if "/av/" in self._driver.get_current_url():
            raise UnwantedArticleException

    @log_function
    def _close_popups_if_needed(self):
        if self.USE_REQUEST_DRIVER:
            return

        self.logger.debug(f"Trying to click close popups if needed")
        self._try_click_element(by=By.XPATH, value=BBCXPaths.popup_close_button, raise_on_fail=False)

    def get_new_article_urls_from_home_page(self) -> List[str]:
        self._get_page(self._homepage_url)
        articles_urls = set()
        articles_elements = self._driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'gel-layout__item')]/.//a[contains(@href, '/news/') or contains(@href, '/article/')]")
        for element in articles_elements:
            href = element.get_attribute("href")
            # todo: order filtering
            if self._homepage_url in href and bool(re.search(r'\d', href) and not ("#comp" in href)) and not ("/av/" in href):
                articles_urls.add(href)
        return list(articles_urls)

    def get_article(self, task: Task) -> Article:
        self._get_page(url=task.url)
        self._check_unwanted_article()
        self._close_popups_if_needed()

        article_id = uuid4()
        url = task.url
        domain = task.domain
        title = self._get_article_title()
        content = self._get_article_content_text()
        # publishing_time: datetime.datetime
        # collecting_time: datetime.datetime
        # task_id: Optional[str] = None
        # category: Optional[str] = None
        # images: Optional[List[str]] = None
        # state: Optional[str] = None
        # pass
        # return
