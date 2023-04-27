from datetime import datetime
from time import sleep
from typing import List
from uuid import uuid4

from pymongo.errors import ConnectionFailure

from db_driver import get_current_db_driver
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.db_objects.task import Task
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import DataNotFoundDBException, UpdateDataDBException, InsertDataDBException
from logger import get_current_logger
from scrapers import websites_scrapers_factory
from scrapers.websites_scrapers.utils.consts import MainConsts


class LogicScaper:
    SLEEPING_TIME = 60 * 15

    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()

    def _get_task_by_status(self, status: str):
        try:
            task: dict = self._db.get_one(table_name=DBConsts.TASKS_TABLE_NAME, data_filter={"status": status})
            task_object: Task = get_db_object_from_dict(task, Task)
            return task_object
        except DataNotFoundDBException:
            return None

    def _get_new_task(self) -> Task:
        for status in ["pending", "failed"]:
            task = self._get_task_by_status(status=status)
            if task:
                return task

    def _update_task_status(self, task_id: str, status: str):
        try:
            data_filter = {"task_id": task_id}
            new_data = {"status": status}
            self._db.update_one(table_name=DBConsts.TASKS_TABLE_NAME, data_filter=data_filter, new_data=new_data)
        except UpdateDataDBException as e:
            desc = f"Error updating task as `running`"
            self.logger.error(desc)
            raise e

    def _filter_only_not_exits_articles(self, urls: List[str]) -> List[str]:
        data_filter = {"url": {"$in": urls}}
        exists_articles = self._db.get_many(table_name=DBConsts.ARTICLE_TABLE_NAME, data_filter=data_filter)
        exists_articles_urls = {exists_article.get("url") for exists_article in exists_articles}
        new_articles = list(set(urls).difference(exists_articles_urls))
        return new_articles

    def _create_new_task(self, url: str, domain: str):
        for trie in range(MainConsts.TIMES_TRY_CREATE_TASK):
            try:
                task_data = {
                    "task_id": str(uuid4()),
                    "url": url,
                    "domain": domain,
                    "status": "pending",
                    "type": MainConsts.COLLECT_ARTICLE,
                    "creation_time": datetime.now()
                }
                new_task: dict = Task(**task_data).convert_to_dict()
                inserted_id = self._db.insert_one(table_name=DBConsts.TASKS_TABLE_NAME, data=new_task)
                self.logger.info(f"Created new task inserted_id: {inserted_id}")
                return
            except Exception as e:
                self.logger.warning(f"Error create new task NO. {trie}/{MainConsts.TIMES_TRY_CREATE_TASK} - {str(e)}")
                continue
        desc = f"Error creating new task into db after {MainConsts.TIMES_TRY_CREATE_TASK} tries"
        raise InsertDataDBException(desc)

    def _handle_task(self, task: Task):
        if task.type == MainConsts.COLLECT_URLS:
            website_scraper = websites_scrapers_factory(scraper_name=task.domain)
            urls = website_scraper.get_new_article_urls_from_home_page()
            urls = self._filter_only_not_exits_articles(urls=urls)
            for url in urls:
                try:
                    self._create_new_task(url=url, domain=task.domain)
                except Exception as e:
                    desc = f"Error creating new task with type: {MainConsts.COLLECT_ARTICLE} - {str(e)}"
                    self.logger.error(desc)
        elif task.type == MainConsts.COLLECT_ARTICLE:
            pass

    def run(self):
        while True:
            try:
                task = self._get_new_task()
                if task:
                    self._update_task_status(task_id=task.task_id, status="running")
                    self._handle_task(task=task)
                else:
                    self.logger.debug(f"Couldn't find task, sleeping for {self.SLEEPING_TIME / 60} minutes")
                    sleep(self.SLEEPING_TIME)
            except ConnectionFailure as e:
                self.logger.warning(f"Error connecting to db, initialize the db again - {str(e)}")
                self._db = get_current_db_driver()
            except Exception as e:
                self.logger.warning(f"Error handle task - {str(e)}")


if __name__ == '__main__':
    logic_scraper = LogicScaper()
    logic_scraper.run()
