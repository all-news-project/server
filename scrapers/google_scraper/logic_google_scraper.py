import random
from datetime import datetime, timedelta
from time import sleep
from typing import List
from uuid import uuid4

from GoogleNews import GoogleNews
from selenium.webdriver.common.by import By

from db_driver.db_objects.article import Article
from db_utils.article_utils import ArticleUtils
from db_utils.cluster_utils import ClusterUtils
from db_utils.server_consts import ServerTimeConsts
from db_utils.web_utils import extract_domain_from_url
from logger import get_current_logger, log_function
from scrapers.google_scraper.utils.consts import GoogleScraperConsts
from scrapers.google_scraper.utils.xpaths import TrendXPaths
from scrapers.web_scraper.scraper_drivers import get_scraping_driver
from scrapers.web_scraper.websites_scrapers.utils.exceptions import FailedGetArticleException


class LogicGoogleScraper:
    SEC_TO_SLEEP = ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES * 6  # 6 hours

    def __init__(self):
        self.logger = get_current_logger(task_type="google scraper logic")
        self._article_utils = ArticleUtils()
        self._cluster_utils = ClusterUtils()
        self._driver = get_scraping_driver(via_request=True)
        self._google_news = GoogleNews()
        self.__set_google_news_language()
        self.__set_google_news_dates()
        self.__set_google_news_encoding()

    @log_function
    def __set_google_news_language(self):
        self._google_news.set_lang(GoogleScraperConsts.DEFAULT_ARTICLES_LANGUAGE)

    @log_function
    def __set_google_news_dates(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        google_string_start_time = f"{start_time.month}/{start_time.day}/{start_time.year}"
        google_string_end_time = f"{end_time.month}/{end_time.day}/{end_time.year}"
        self._google_news.set_time_range(start=google_string_start_time, end=google_string_end_time)

    @log_function
    def __set_google_news_encoding(self):
        self._google_news.set_encode(GoogleScraperConsts.ARTICLES_ENCODING)

    @staticmethod
    def __clear_trend_text(text: str) -> str:
        if "(" in text:
            text = text.split("(")[0]
        text = text.replace(".", "")
        text = text.replace("&", "and")
        text = text.strip()
        return text

    @staticmethod
    def __is_trend_text_valid(text: str) -> bool:
        if text.isnumeric():
            return False
        return True

    @log_function
    def _get_popular_trends(self) -> List[str]:
        trends: List[str] = []
        self._driver.get_url(GoogleScraperConsts.TREND_WEBSITE_URL)
        elements = self._driver.find_elements(by=By.XPATH, value=TrendXPaths.trends_link)
        for element in elements:
            text: str = self.__clear_trend_text(element.text)
            if self.__is_trend_text_valid(text=text):
                trends.append(text)

        self.logger.info(f"Collected {len(trends)} trends")
        return trends

    def __create_article_from_google_article(self, google_article: dict) -> Article:
        self.logger.debug(google_article)
        data = {
            "article_id": str(uuid4()),
            "url": google_article["link"],
            "domain": extract_domain_from_url(url=google_article["link"]),
            "title": google_article["title"],
            "content": google_article["desc"],
            "publishing_time": google_article["datetime"],
            "collecting_time": datetime.now(),
            "images": [],
            "scraping_type": "google"
        }
        article = Article(**data)
        return article

    @log_function
    def _get_google_articles(self, trend: str) -> List[Article]:
        articles: List[Article] = []
        self._google_news.search(key=trend)
        results = self._google_news.results()

        if len(results) < GoogleScraperConsts.MIN_RESULTS_FOR_CLUSTER:
            desc = f"Cannot find at list {GoogleScraperConsts.MIN_RESULTS_FOR_CLUSTER} articles for trend: {trend}"
            raise FailedGetArticleException(desc)

        self.logger.debug(f"Got {len(results)} google articles for trend: `{trend}`")
        for google_article in results:
            try:
                article: Article = self.__create_article_from_google_article(google_article=google_article)
                articles.append(article)
            except Exception as e:
                desc = f"Error creating article for google result article, except: {str(e)}"
                self.logger.warning(desc)
        self._google_news.clear()
        return articles

    @log_function
    def handle_new_google_articles(self, articles: List[Article], trend: str):
        # trend cluster already exists -> add articles to cluster (the ones that not in it)
        cluster = self._cluster_utils.get_cluster_by_trend(trend=trend)
        if cluster:
            for article in articles:
                if self._article_utils.get_article_by_url(article_url=article.url):
                    self.logger.warning(f"Article `{article.article_id}` already exists")
                    continue
                self._article_utils.insert_article(article=article)
                self.logger.info(f"Created google article: `{article.title}` -> `{article.article_id}`")
                self._cluster_utils.add_article_to_cluster(cluster=cluster, article=article)
        # Create new cluster
        else:
            cluster_articles: List[Article] = []
            for article in articles:
                if self._article_utils.get_article_by_url(article_url=article.url):
                    self.logger.warning(f"Article `{article.article_id}` already exists")
                    continue
                self._article_utils.insert_article(article=article)
                cluster_articles.append(article)
                self.logger.info(f"Created google article: `{article.title}` -> `{article.article_id}`")
            cluster = self._cluster_utils.create_cluster_from_articles_list(articles=cluster_articles, trend=trend)
            self.logger.info(f"Created cluster with {len(cluster_articles)} google articles -> `{cluster.cluster_id}`")

    @log_function
    def run(self):
        while True:
            popular_trends = self._get_popular_trends()
            popular_trends = random.sample(popular_trends, GoogleScraperConsts.AMOUNT_SAMPLES_TRENDS)
            for trend in popular_trends:
                try:
                    articles: List[Article] = self._get_google_articles(trend=trend)
                    self.handle_new_google_articles(articles=articles, trend=trend)
                except FailedGetArticleException:
                    self.logger.warning(f"Error finding articles for trend: `{trend}`")
                    continue
                except Exception as e:
                    self.logger.error(f"Error running logic google scraper for trend: `{trend}`, except: {str(e)}")
                    continue
            self.logger.info(f"Done collecting google articles")
            desc = f"sleeping for {self.SEC_TO_SLEEP / (ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES)} hours"
            self.logger.warning(desc)
            sleep(self.SEC_TO_SLEEP)
