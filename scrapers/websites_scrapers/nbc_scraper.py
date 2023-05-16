import re
from datetime import datetime
from typing import List, Union

from selenium.webdriver.common.by import By

from logger import log_function
from scrapers.websites_scrapers.utils.xpaths import NBCXPaths
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase
from scrapers.websites_scrapers.utils.consts import ScraperConsts, NBCConsts


class NBCScraper(WebsiteScraperBase):

    def __init__(self):
        super().__init__()
        self._homepage_url = ScraperConsts.TIME_HOME_PAGE

    @log_function
    def _extract_article_urls_from_home_page(self) -> List[str]:
        articles_urls = set()
        articles_elements = self._driver.find_elements(by=By.XPATH, value=NBCXPaths.articles_elements)
        for element in articles_elements:
            href = element.get_attribute("href")
            is_url_filter_bad = any([url_filter in href for url_filter in NBCConsts.NEW_ARTICLE_URL_FILTER])
            if is_url_filter_bad:
                continue

            #if self._homepage_url in href and bool(re.search(r'\d', href)):
            #    articles_urls.add(href)
        return list(articles_urls)

    @log_function
    def _get_article_title(self) -> str:
        pass

    @log_function
    def _get_article_content_text(self) -> str:
        pass

    @log_function
    def _get_article_publishing_time(self) -> Union[datetime, object]:
        pass

    @log_function
    def _get_article_image_urls(self) -> List[str]:
        pass

    @log_function
    def _check_unwanted_article(self):
        pass
    @log_function
    def _close_popups_if_needed(self):
        pass