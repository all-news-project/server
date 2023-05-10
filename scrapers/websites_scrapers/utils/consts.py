import os


class ScraperConsts:
    BBC_HOME_PAGE = "https://www.bbc.com/news/"


class MainConsts:
    COLLECT_URLS = "collect_urls"
    COLLECT_ARTICLE = "collect_article"
    TIMES_TRY_GET_PAGE = int(os.getenv(key="TIMES_TO_TRY_GET_HOMEPAGE", default=3))
    TIMES_TRY_CLICK_ELEMENT = int(os.getenv(key="TIMES_TRY_CLICK_ELEMENT", default=3))
    ELEMENT_TIMEOUT = int(os.getenv(key="ELEMENT_TIMEOUT", default=5))
