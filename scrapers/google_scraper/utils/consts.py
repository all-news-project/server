import os


class GoogleScraperConsts:
    AMOUNT_SAMPLES_TRENDS = int(os.getenv(key="AMOUNT_SAMPLES_TRENDS", default=50))
    TREND_WEBSITE_URL = "https://mclennan.libguides.com/issues/popular_issues"
    DEFAULT_ARTICLES_LANGUAGE = os.getenv(key="DEFAULT_ARTICLES_LANGUAGE", default="en")
    ARTICLES_ENCODING = os.getenv(key="ARTICLES_ENCODING", default="utf-8")
    MIN_RESULTS_FOR_CLUSTER = int(os.getenv(key="MIN_RESULTS_FOR_CLUSTER", default=3))


class IconsScraperConsts:
    TIMES_TO_TRY_GET_ICONS_FROM_PAGE = 3
    SAVE_IMG = bool(os.getenv(key="SAVE_ING", default=True))
    URL = "https://news.google.com/"
    SAVE_TO_DB = bool(os.getenv(key="SAVE_TO_DB", default=True))
    CRITICAL_ELEMENT_TIMEOUT = int(os.getenv(key="CRITICAL_ELEMENT_TIMEOUT", default=20))
