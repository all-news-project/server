import os
from datetime import datetime
from typing import List, Union
from uuid import uuid4

from selenium.common import TimeoutException

from db_driver.db_objects.article import Article
from db_driver.db_objects.task import Task
from logger import get_current_logger, log_function
from scrapers.scraper_drivers import get_scraping_driver
from scrapers.scraper_drivers.utils.exceptions import ErrorClickElementException
from scrapers.websites_scrapers.utils.consts import MainConsts
from scrapers.websites_scrapers.utils.exceptions import FailedGetURLException


class WebsiteScraperBase:
    USE_REQUEST_DRIVER = bool(os.getenv(key="USE_REQUEST_DRIVER", default=False))
    HEADLESS = bool(os.getenv(key="HEADLESS", default=False))

    def __init__(self):
        self._driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        self.logger = get_current_logger()

    @log_function
    def _get_page(self, url: str):
        exception = None
        for trie in range(MainConsts.TIMES_TRY_GET_PAGE):
            try:
                self._driver.get_url(url=url)
                self.logger.info(f"Successfully get to page -> `{url}`")
                return
            except Exception as e:
                exception = e
                desc = f"Cannot get into page try NO. {trie + 1}/{MainConsts.TIMES_TRY_GET_PAGE} - {str(e)}"
                self.logger.warning(desc)
        desc = f"Failed get page -> {url} after {MainConsts.TIMES_TRY_GET_PAGE} tries - {exception}"
        self.logger.error(desc)
        raise FailedGetURLException(desc)

    @log_function
    def _is_element_exists(self, by, value, timeout: int = MainConsts.ELEMENT_TIMEOUT) -> bool:
        try:
            self._driver.wait_until_object_appears(by=by, value=value, timeout=timeout)
            self.logger.info(f"Found element: `{str(value)}`")
            return True
        except TimeoutException:
            self.logger.warning(f"Cannot find element: `{str(value)}`")
            return False

    @log_function
    def _try_click_element(self, by, value, times_to_try: int = MainConsts.TIMES_TRY_CLICK_ELEMENT,
                           timeout: int = MainConsts.ELEMENT_TIMEOUT, raise_on_fail: bool = True):
        for tries in range(times_to_try):
            if not self._is_element_exists(by=by, value=value, timeout=timeout):
                return

            try:
                self._driver.click_on_element(by=by, value=value)
            except Exception as e:
                self.logger.warning(f"Failed click on element NO. {tries}/{times_to_try + 1} - {str(e)}")
        if raise_on_fail:
            raise ErrorClickElementException(f"Failed click in element after {times_to_try + 1} tries")

    @log_function
    def get_article(self, task: Task) -> Article:
        self._get_page(url=task.url)
        self._check_unwanted_article()
        self._close_popups_if_needed()
        data = {
            "article_id": str(uuid4()),
            "url": task.url,
            "domain": task.domain,
            "title": self._get_article_title(),
            "content": self._get_article_content_text(),
            "publishing_time": self._get_article_publishing_time(),
            "collecting_time": datetime.now(),
            "task_id": task.task_id,
            "images": self._get_article_image_urls()
        }
        return Article(**data)

    def _get_article_title(self) -> str:
        raise NotImplementedError

    def _get_article_content_text(self) -> str:
        raise NotImplementedError

    def _get_article_publishing_time(self) -> Union[datetime, object]:
        raise NotImplementedError

    def _get_article_image_urls(self) -> List[str]:
        raise NotImplementedError

    def _check_unwanted_article(self):
        raise NotImplementedError

    def _close_popups_if_needed(self):
        raise NotImplementedError

    def get_new_article_urls_from_home_page(self) -> List[str]:
        raise NotImplementedError
