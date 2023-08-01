import os


class GoogleScraperConsts:
    AMOUNT_SAMPLES_TRENDS = int(os.getenv(key="AMOUNT_SAMPLES_TRENDS", default=50))
    TREND_WEBSITE_URL = "https://mclennan.libguides.com/issues/popular_issues"
    DEFAULT_ARTICLES_LANGUAGE = os.getenv(key="DEFAULT_ARTICLES_LANGUAGE", default="en")
    ARTICLES_ENCODING = os.getenv(key="ARTICLES_ENCODING", default="utf-8")
    MIN_RESULTS_FOR_CLUSTER = int(os.getenv(key="MIN_RESULTS_FOR_CLUSTER", default=3))
