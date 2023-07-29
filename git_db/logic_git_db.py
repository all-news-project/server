from datetime import datetime
from time import sleep
from typing import List

from git_db.utils.git_handler import GitHandler
from git_db.utils.json_handler import save_data_to_json
from server_utils.db_driver.db_objects.article import Article
from server_utils.db_driver.db_objects.cluster import Cluster
from server_utils.db_utils.article_utils import ArticleUtils
from server_utils.db_utils.cluster_utils import ClusterUtils
from server_utils.db_utils.server_consts import ServerTimeConsts
from server_utils.logger import get_current_logger, log_function


class LogicGitDB:
    SEC_TO_SLEEP = ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES * 12  # 12 hours

    def __init__(self):
        self.logger = get_current_logger(task_type="logic_git_db")
        self._git_handler = GitHandler()
        self._article_utils = ArticleUtils()
        self._cluster_utils = ClusterUtils()

    @log_function
    def update_git_data_files_from_db(self):
        articles = self._article_utils.get_all_articles()
        self._save_collection_data_into_json_file(collection_data_list=articles, file_name="articles.json")
        clusters = self._cluster_utils.get_all_clusters()
        self._save_collection_data_into_json_file(collection_data_list=clusters, file_name="clusters.json")

    @log_function
    def _save_collection_data_into_json_file(self, collection_data_list: List[Article | Cluster], file_name: str):
        data_dicts = [data.convert_to_dict_for_json() for data in collection_data_list]
        save_data_to_json(file_name=file_name, data=data_dicts)

    @log_function
    def run(self):
        while True:
            start_time = datetime.now()

            self.logger.debug(f"Start updating git db files")

            # Clone if needed (first time)
            self._git_handler.clone_repo_if_needed()

            # Update repo
            self._git_handler.update_repo()

            # Update repo files from db
            self.update_git_data_files_from_db()

            # # Save repo into GitHub
            self._git_handler.save_repo(f"Update {datetime.now()}")

            total_seconds = (datetime.now() - start_time).total_seconds()

            self.logger.info(f"Done updating git db data, total seconds: {total_seconds}")
            desc = f"sleeping for {self.SEC_TO_SLEEP / (ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES)} hours"
            self.logger.warning(desc)
            sleep(self.SEC_TO_SLEEP)
