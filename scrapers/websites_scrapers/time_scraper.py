import re
from datetime import datetime
from typing import List, Union

from selenium.webdriver.common.by import By

from logger import log_function
from scrapers.websites_scrapers.utils.xpaths import TIMEXPaths
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase
from scrapers.websites_scrapers.utils.consts import ScraperConsts, TIMEConsts


class TIMEScraper(WebsiteScraperBase):
    def __init__(self):
        super().__init__()
        self._homepage_url = ScraperConsts.TIME_HOME_PAGE

    def _get_article_title(self) -> str:
        pass

    def _get_article_content_text(self) -> str:
        pass

    def _get_article_publishing_time(self) -> Union[datetime, object]:
        pass

    def _get_article_image_urls(self) -> List[str]:
        pass

    def _check_unwanted_article(self):
        pass

    @log_function
    def _close_popups_if_needed(self):
        if self.USE_REQUEST_DRIVER:
            return

        self.logger.debug(f"Trying to click close popups if needed")
        self._try_click_element(by=By.XPATH, value=TIMEXPaths.popup_close_button, raise_on_fail=False)

    def _extract_article_urls_from_home_page(self) -> List[str]:
        articles_urls = set()
        articles_elements = self._driver.find_elements(by=By.XPATH, value=TIMEXPaths.articles_elements)
        for element in articles_elements:
            href = element.get_attribute("href")
            is_url_filter_bad = any([url_filter in href for url_filter in TIMEConsts.NEW_ARTICLE_URL_FILTER])
            if is_url_filter_bad:
                continue

            if self._homepage_url in href and bool(re.search(r'\d', href)):
                articles_urls.add(href)
        return list(articles_urls)
