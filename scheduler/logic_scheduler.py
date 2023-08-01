from time import sleep

from db_driver import get_current_db_driver
from logger import get_current_logger, log_function
from scrapers.websites_scrapers.utils.consts import ScraperConsts, MainConsts
from db_utils.server_consts import ServerTimeConsts
from db_utils.task_utils import TaskUtils


class LogicScheduler:
    SEC_TO_SLEEP = ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES * 12  # 12 hours

    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self.task_utils = TaskUtils()

    @log_function
    def _create_collect_urls_task(self, url: str, domain: str):
        try:
            self.logger.debug(f"Creating collect urls task for `{domain}`m url: `{url}`")
            self.task_utils.create_new_task(url=url, domain=domain, task_type=MainConsts.COLLECT_URLS)
            self.logger.info(f"Created collect url task")
        except Exception as e:
            self.logger.error(f"Error create collect urls task for `{domain}`, url: `{url}`, except: {str(e)}")

    @log_function
    def run(self):
        """
        Create collect urls tasks every 12 hours
        :return:
        """
        while True:
            self.logger.debug(f"Start creating tasks")
            for domain, url in ScraperConsts.DOMAINS_HOME_PAGE_URLS.items():
                self._create_collect_urls_task(url=url, domain=domain)
            domains = ScraperConsts.DOMAINS_HOME_PAGE_URLS.keys()
            self.logger.info(f"Done creating collect urls tasks for domains: `{domains}`")
            desc = f"sleeping for {self.SEC_TO_SLEEP / (ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES)} hours"
            self.logger.warning(desc)
            sleep(self.SEC_TO_SLEEP)
