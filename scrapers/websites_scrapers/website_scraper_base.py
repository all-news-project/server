from datetime import datetime
from typing import List

from db_driver.db_objects.article import Article


class WebsiteScraperBase:
    def _get_home_page(self):
        raise NotImplementedError

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
        raise NotImplementedError

    def get_article(self, url: str) -> Article:
        raise NotImplementedError
