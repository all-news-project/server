import os


class ScraperConsts:
    BBC_HOME_PAGE = "https://www.bbc.com/news/"
    TIME_HOME_PAGE = "https://time.com/"
    CNN_HOME_PAGE = "https://cnn.com/"
    NBC_HOME_PAGE = "https://www.nbcnews.com/"
    DOMAINS_HOME_PAGE_URLS = {"bbc": BBC_HOME_PAGE, "time": TIME_HOME_PAGE, "cnn": CNN_HOME_PAGE,"nbc": NBC_HOME_PAGE}


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


class CNNConsts:
    NEW_ARTICLE_URL_FILTER_WANTED = ["/politics/", "/africa/", "/americas/", "/asia/", "/australia/", "/china/",
                                     "/europe/", "/india/", "/middleeast/", "/uk/"]
    NEW_ARTICLE_URL_FILTER_UNWANTED = ["/gallery/", "/videos/"]
    PUBLISHING_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    CNN_SCRAPE_PAGES = ["https://cnn.com/politics", "https://cnn.com/world"]


class MainConsts:
    COLLECT_URLS = "collect_urls"
    COLLECT_ARTICLE = "collect_article"
    TIMES_TRY_GET_PAGE = int(os.getenv(key="TIMES_TO_TRY_GET_HOMEPAGE", default=3))
    TIMES_TRY_CLICK_ELEMENT = int(os.getenv(key="TIMES_TRY_CLICK_ELEMENT", default=3))
    ELEMENT_TIMEOUT = int(os.getenv(key="ELEMENT_TIMEOUT", default=5))
