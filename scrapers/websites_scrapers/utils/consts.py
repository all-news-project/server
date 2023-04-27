import os


class ScraperConsts:
    BBC_HOME_PAGE = "https://www.bbc.com/"


class MainConsts:
    COLLECT_URLS = "collect_urls"
    COLLECT_ARTICLE = "collect_article"
    TIMES_TRY_CREATE_TASK = int(os.getenv(key="TIMES_TRY_CREATE_TASK", default=3))
    TIMES_TRY_GET_HOMEPAGE = int(os.getenv(key="TIMES_TO_TRY_GET_HOMEPAGE", default=3))
