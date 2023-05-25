from time import sleep
from typing import List, Tuple

from pymongo.errors import ConnectionFailure

from db_driver import get_current_db_driver
from db_driver.db_objects.task import Task
from db_driver.utils.consts import DBConsts
from logger import get_current_logger, log_function
from scrapers import websites_scrapers_factory
from scrapers.websites_scrapers.utils.consts import MainConsts
from scrapers.websites_scrapers.utils.exceptions import UnwantedArticleException
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.db_utils.task_utils import TaskUtils
from server_utils.server_consts import ScheduleConsts, TaskConsts


class LogicScaper:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self.task_utils = TaskUtils()
        self.article_utils = ArticleUtils()

    @log_function
    def _filter_only_not_exits_articles(self, urls: List[str]) -> List[str]:
        data_filter = {"url": {"$in": urls}}
        # todo: also check with `unwanted` tasks status
        exists_articles = self._db.get_many(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)
        exists_articles_urls = {exists_article.get("url") for exists_article in exists_articles}
        new_articles = list(set(urls).difference(exists_articles_urls))
        return new_articles

    @log_function
    def _create_collecting_article_tasks(self, urls: List[str], domain: str):
        for url in urls:
            try:
                self.task_utils.create_new_task(url=url, domain=domain, task_type=MainConsts.COLLECT_ARTICLE)
            except Exception as e:
                desc = f"Error creating new task with type: {MainConsts.COLLECT_ARTICLE} - {str(e)}"
                self.logger.error(desc)

    @log_function
    def _handle_task(self, task: Task) -> Tuple[str, str]:
        try:
            website_scraper = websites_scrapers_factory(scraper_name=task.domain)
            if task.type == MainConsts.COLLECT_URLS:
                urls = website_scraper.get_new_article_urls_from_home_page()
                urls = self._filter_only_not_exits_articles(urls=urls)
                self._create_collecting_article_tasks(urls=urls, domain=task.domain)

            elif task.type == MainConsts.COLLECT_ARTICLE:
                article = website_scraper.get_article(task=task)
                self.article_utils.insert_article(article=article)

            self.logger.info(f"Done handle task of type: `{task.type}`")
        except UnwantedArticleException:
            desc = f"Article is Unwanted: `{task.task_id}` change task status to: `{TaskConsts.UNWANTED}`"
            self.logger.warning(desc)
            return TaskConsts.UNWANTED, TaskConsts.DESC_UNWANTED

        except Exception as e:
            desc = f"Failed run task task_id: `{task.task_id}`, type: `{task.type}` - {str(e)}"
            self.logger.error(desc)
            return TaskConsts.FAILED, desc

        return TaskConsts.SUCCEEDED, TaskConsts.DESC_SUCCEEDED

    @log_function
    def run(self):
        while True:
            try:
                task = self.task_utils.get_new_task()
                if task:
                    self.logger = get_current_logger(task_id=task.task_id, task_type=task.type)
                    self.task_utils.update_task_status(task=task, status=TaskConsts.RUNNING)
                    task_status, desc = self._handle_task(task=task)
                    self.task_utils.update_task_status(task=task, status=task_status, desc=desc)
                else:
                    self.logger.warning(f"Couldn't find task, sleeping for {ScheduleConsts.SLEEPING_TIME / 60} minutes")
                    sleep(ScheduleConsts.SLEEPING_TIME)
            except ConnectionFailure as e:
                self.logger.warning(f"Error connecting to db, initialize the db again - {str(e)}")
                self._db = get_current_db_driver()
            except Exception as e:
                self.logger.warning(f"Error handle task - {str(e)}")
