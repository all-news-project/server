import os


class ScraperConsts:
    BBC_HOME_PAGE = "https://www.bbc.com/news/"
    TIME_HOME_PAGE = "https://time.com/"
    NBC_HOME_PAGE = "https://www.nbcnews.com/"


class BBCConsts:
    NEW_ARTICLE_URL_FILTER = ["#comp", "/av/"]
    PUBLISHING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    TITLE_FILTER = " - BBC News"


class TIMEConsts:
    TITLE_FILTER = " | Time"
    PUBLISHING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    NEW_ARTICLE_URL_FILTER = []


class NBCConsts:
    PUBLISHING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    NEW_ARTICLE_URL_FILTER = []


class MainConsts:
    COLLECT_URLS = "collect_urls"
    COLLECT_ARTICLE = "collect_article"
    TIMES_TRY_GET_PAGE = int(os.getenv(key="TIMES_TO_TRY_GET_HOMEPAGE", default=3))
    TIMES_TRY_CLICK_ELEMENT = int(os.getenv(key="TIMES_TRY_CLICK_ELEMENT", default=3))
    ELEMENT_TIMEOUT = int(os.getenv(key="ELEMENT_TIMEOUT", default=5))
