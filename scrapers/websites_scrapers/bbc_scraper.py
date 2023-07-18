import re
from datetime import datetime
from typing import List, Union

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from scrapers.websites_scrapers.utils.exceptions import UnwantedArticleException
from scrapers.websites_scrapers.utils.xpaths import BBCXPaths
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase
from scrapers.websites_scrapers.utils.consts import ScraperConsts, BBCConsts
from server_utils import log_function


class BBCScraper(WebsiteScraperBase):
    def __init__(self):
        super().__init__()
        self._homepage_url = ScraperConsts.BBC_HOME_PAGE

    @log_function
    def _get_article_title(self) -> str:
        title = self._driver.get_title().replace(BBCConsts.TITLE_FILTER, "")
        self.logger.info(f"Got title: `{title}`")
        return title

    @log_function
    def _get_article_content_text(self) -> str:
        paragraphs = self._driver.find_elements(by=By.XPATH, value=BBCXPaths.text_block)
        if not paragraphs:
            desc = f"Error find content text of article, element value: `{BBCXPaths.text_block}`"
            self.logger.error(desc)
            raise NoSuchElementException(desc)
        else:
            return " ".join([paragraph.get_text() for paragraph in paragraphs])

    @log_function
    def _get_article_publishing_time(self) -> Union[datetime, None]:
        try:
            time_element = self._driver.find_element(by=By.XPATH, value=BBCXPaths.publishing_time_element)
            publishing_timestamp = time_element.get_attribute("datetime")
            publishing_datetime = datetime.strptime(publishing_timestamp, BBCConsts.PUBLISHING_FORMAT)
            return publishing_datetime
        except Exception as e:
            self.logger.warning(f"Error collecting publishing time - {e}")
            return None

    @log_function
    def _get_article_image_urls(self) -> List[str]:
        image_urls = []
        images = self._driver.find_elements(by=By.XPATH, value=BBCXPaths.article_image)
        for image in images:
            image_urls.append(image.get_attribute("src"))
        return image_urls

    @log_function
    def _check_unwanted_article(self):
        self.logger.debug(f"_check_unwanted_article, current -> `{self._driver.get_current_url()}`")
        if "/av/" in self._driver.get_current_url():
            raise UnwantedArticleException(f"Article is unwanted -> `{self._driver.get_current_url()}`")

    @log_function
    def _close_popups_if_needed(self):
        if self.USE_REQUEST_DRIVER:
            return

        self.logger.debug(f"Trying to click close popups if needed")
        self._try_click_element(by=By.XPATH, value=BBCXPaths.popup_close_button, raise_on_fail=False)

    @log_function
    def _extract_article_urls_from_home_page(self) -> List[str]:
        articles_urls = set()
        articles_elements = self._driver.find_elements(by=By.XPATH, value=BBCXPaths.articles_elements)
        for element in articles_elements:
            href = element.get_attribute("href")
            is_url_filter_bad = any([url_filter in href for url_filter in BBCConsts.NEW_ARTICLE_URL_FILTER])
            if is_url_filter_bad:
                continue

            if self._homepage_url in href and bool(re.search(r'\d', href)):
                articles_urls.add(href)
        return list(articles_urls)
