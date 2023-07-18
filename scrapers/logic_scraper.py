from time import sleep
from typing import List, Tuple

from server_utils import get_current_logger, log_function
from server_utils.db_driver.db_objects.status_timestamp import StatusTimestamp
from scrapers import websites_scrapers_factory
from scrapers.websites_scrapers.utils.consts import MainConsts
from scrapers.websites_scrapers.utils.exceptions import UnwantedArticleException, FailedConstantlyArticleException, \
    FailedGetURLException
from server_utils.db_driver.db_objects.task import Task
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.db_utils.task_utils import TaskUtils
from server_utils.server_consts import ScheduleConsts, TaskConsts


class LogicScaper:
    def __init__(self):
        self.logger = get_current_logger()
        self.task_utils = TaskUtils()
        self.article_utils = ArticleUtils()

    @log_function
    def _filter_only_not_exits_articles(self, urls: List[str], domain: str) -> List[str]:
        # Already collected articles in db
        exists_articles = self.article_utils.get_articles_by_urls(urls=urls)
        articles_urls = {exists_article.url for exists_article in exists_articles}

        # Unwanted articles from tasks
        exists_unwanted_tasks = self.task_utils.get_unwanted_articles_by_domain(domain=domain)
        unwanted_tasks_urls = {exists_unwanted_task.url for exists_unwanted_task in exists_unwanted_tasks}

        # Already running tasks
        exists_running_tasks = self.task_utils.get_unwanted_articles_by_domain(domain=domain, status=TaskConsts.RUNNING)
        running_tasks_urls = {exists_running_task.url for exists_running_task in exists_running_tasks}

        all_exists_urls: set = articles_urls.union(unwanted_tasks_urls).union(running_tasks_urls)
        new_articles = list(set(urls).difference(all_exists_urls))
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
    def _check_task_failed_constantly(self, task: Task):
        # Task status_timestamp
        status_timestamp: List[StatusTimestamp] = self.task_utils.get_task_status_timestamp(task=task)

        # Other task with same url (same task)
        other_tasks: List[Task] = self.task_utils.get_tasks_by_url(url=task.url)
        for other_task in other_tasks:
            status_timestamp.extend(self.task_utils.get_task_status_timestamp(task=other_task))

        times_task_has_failed = self.task_utils.count_amount_failed_task_in_timestamp(status_timestamp=status_timestamp)
        if times_task_has_failed > TaskConsts.MAX_TIME_FAILED:
            desc = f"Task: `{task.task_id}` has failed more than {TaskConsts.MAX_TIME_FAILED} times, set as unwanted"
            self.logger.error(desc)
            raise FailedConstantlyArticleException(desc)

    @log_function
    def _handle_task(self, task: Task) -> Tuple[str, str]:
        website_scraper = None
        try:
            self._check_task_failed_constantly(task=task)
            website_scraper = websites_scrapers_factory(scraper_name=task.domain)
            if task.type == MainConsts.COLLECT_URLS:
                urls = website_scraper.get_new_article_urls_from_home_page()
                urls = self._filter_only_not_exits_articles(urls=urls, domain=task.domain)
                self._create_collecting_article_tasks(urls=urls, domain=task.domain)

            elif task.type == MainConsts.COLLECT_ARTICLE:
                article = website_scraper.get_article(task=task)
                self.article_utils.insert_article(article=article)

            self.logger.info(f"Done handle task of type: `{task.type}`")
        except UnwantedArticleException:
            desc = f"Article is Unwanted: `{task.task_id}` change task status to: `{TaskConsts.UNWANTED}`"
            self.logger.warning(desc)
            return TaskConsts.UNWANTED, TaskConsts.DESC_UNWANTED

        except FailedConstantlyArticleException:
            desc = f"Article failed to collect after {TaskConsts.MAX_TIME_FAILED} tries"
            self.logger.warning(desc)
            return TaskConsts.FAILED_CONSTANTLY, desc

        except FailedGetURLException as e:
            desc = e.msg
            self.logger.error(desc)
            return TaskConsts.FAILED_GET_URL, desc

        except Exception as e:
            desc = f"Failed run task task_id: `{task.task_id}`, type: `{task.type}` - {str(e)}"
            self.logger.error(desc)
            if website_scraper:
                website_scraper.quit_driver()
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
            except Exception as e:
                self.logger.warning(f"Error handle task - {str(e)}")
