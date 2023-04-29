from time import sleep
from typing import List

from pymongo.errors import ConnectionFailure

from db_driver import get_current_db_driver
from db_driver.db_objects.task import Task
from db_driver.utils.consts import DBConsts
from logger import get_current_logger, log_function
from scrapers import websites_scrapers_factory
from scrapers.websites_scrapers.utils.consts import MainConsts
from server_utils.db_utils.task_utils import TaskUtils


class LogicScaper:
    SLEEPING_TIME = 60 * 15

    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self.task_utils = TaskUtils()

    @log_function
    def _filter_only_not_exits_articles(self, urls: List[str]) -> List[str]:
        data_filter = {"url": {"$in": urls}}
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
    def _handle_task(self, task: Task) -> bool:
        try:
            if task.type == MainConsts.COLLECT_URLS:
                website_scraper = websites_scrapers_factory(scraper_name=task.domain)
                urls = website_scraper.get_new_article_urls_from_home_page()
                urls = self._filter_only_not_exits_articles(urls=urls)
                self._create_collecting_article_tasks(urls=urls, domain=task.domain)
                self.logger.info(f"Done handle task of type: `{task.type}`")
            elif task.type == MainConsts.COLLECT_ARTICLE:
                pass
        except Exception as e:
            desc = f"Failed run task task_id: `{task.task_id}`, type: `{task.type}` - {str(e)}"
            self.logger.error(desc)
            return False
        return True

    @log_function
    def run(self):
        while True:
            try:
                task = self.task_utils.get_new_task()
                if task:
                    self.logger = get_current_logger(task_id=task.task_id, task_type=task.type)
                    self.task_utils.update_task_status(task=task, status="running")
                    is_task_succeeded = self._handle_task(task=task)
                    if is_task_succeeded:
                        self.task_utils.update_task_status(task=task, status="succeeded")
                    else:
                        self.task_utils.update_task_status(task=task, status="failed")
                else:
                    self.logger.warning(f"Couldn't find task, sleeping for {self.SLEEPING_TIME / 60} minutes")
                    sleep(self.SLEEPING_TIME)
            except ConnectionFailure as e:
                self.logger.warning(f"Error connecting to db, initialize the db again - {str(e)}")
                self._db = get_current_db_driver()
            except Exception as e:
                self.logger.warning(f"Error handle task - {str(e)}")


if __name__ == '__main__':
    logic_scraper = LogicScaper()
    logic_scraper.run()
