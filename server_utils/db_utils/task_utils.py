from datetime import datetime
from typing import List
from uuid import uuid4

from db_driver import get_current_db_driver
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.db_objects.task import Task
from db_driver.db_objects.status_timestamp import StatusTimestamp
from db_driver.utils.consts import DBConsts
from db_driver.utils.exceptions import InsertDataDBException, UpdateDataDBException, DataNotFoundDBException
from logger import get_current_logger, log_function
from server_utils.server_consts import TaskConsts


class TaskUtils:
    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()

    @log_function
    def create_new_task(self, url: str, domain: str, task_type: str):
        for trie in range(TaskConsts.TIMES_TRY_CREATE_TASK):
            try:
                creation_time = datetime.now()
                task_data = {
                    "task_id": str(uuid4()),
                    "url": url,
                    "domain": domain,
                    "status": TaskConsts.PENDING,
                    "type": task_type,
                    "status_timestamp": [StatusTimestamp(status=TaskConsts.PENDING, time_changed=creation_time)],
                    "creation_time": creation_time
                }
                new_task: dict = Task(**task_data).convert_to_dict()
                inserted_id = self._db.insert_one(table_name=DBConsts.TASKS_TABLE_NAME, data=new_task)
                self.logger.info(f"Created new task inserted_id: {inserted_id}")
                return
            except Exception as e:
                self.logger.warning(f"Error create new task NO. {trie}/{TaskConsts.TIMES_TRY_CREATE_TASK} - {str(e)}")
                continue
        desc = f"Error creating new task into db after {TaskConsts.TIMES_TRY_CREATE_TASK} tries"
        raise InsertDataDBException(desc)

    @log_function
    def update_task_status(self, task: Task, status: str, desc: str = None):
        try:
            data_filter = {"task_id": task.task_id}
            new_timestamp = StatusTimestamp(status=status, time_changed=datetime.now(), desc=desc)
            task.status_timestamp.append(new_timestamp.convert_to_dict())
            new_data = {"status": status, "status_timestamp": task.status_timestamp}
            self._db.update_one(table_name=DBConsts.TASKS_TABLE_NAME, data_filter=data_filter, new_data=new_data)
        except UpdateDataDBException as e:
            desc = f"Error updating task task_id: `{task.task_id}` as status: `{status}`"
            self.logger.error(desc)
            raise e

    @log_function
    def _get_task_by_status(self, status: str):
        try:
            self.logger.debug(f"Trying get task by status: `{status}`")
            task: dict = self._db.get_one(table_name=DBConsts.TASKS_TABLE_NAME, data_filter={"status": status})
            task_object: Task = get_db_object_from_dict(task, Task)
            return task_object
        except DataNotFoundDBException:
            return None

    @log_function
    def get_new_task(self) -> Task:
        for status in [TaskConsts.PENDING, TaskConsts.FAILED]:
            task = self._get_task_by_status(status=status)
            if task:
                return task

    @log_function
    def get_unwanted_articles_by_domain(self, domain: str, status: str = None) -> List[Task]:
        unwanted_articles_in_tasks: List[Task] = list()
        try:
            data_filter = {"status": TaskConsts.UNWANTED, "domain": domain}
            if status:
                data_filter.update({"status": status})
            tasks_data = self._db.get_many(table_name=DBConsts.TASKS_TABLE_NAME, data_filter=data_filter)
            for task in tasks_data:
                task_object: Task = get_db_object_from_dict(task, Task)
                unwanted_articles_in_tasks.append(task_object)
        except Exception as e:
            self.logger.error(f"Error getting unwanted articles in tasks by domain, {str(e)}")
        return unwanted_articles_in_tasks

    @log_function
    def get_tasks_by_url(self, url: str) -> List[Task]:
        tasks: List[Task] = []
        try:
            data_filter = {"url": url}
            tasks_dict = self._db.get_many(table_name=DBConsts.TASKS_TABLE_NAME, data_filter=data_filter)
            tasks.extend(self.convert_tasks_dict_to_objects(tasks_dict=tasks_dict))
        except DataNotFoundDBException:
            self.logger.warning(f"Didn't find any task by url: `{url}`")
        return tasks

    @staticmethod
    def get_task_status_timestamp(task: Task) -> List[StatusTimestamp]:
        return [StatusTimestamp(**timestamp) for timestamp in task.status_timestamp if type(timestamp) == dict]

    @staticmethod
    def convert_tasks_dict_to_objects(tasks_dict: List[dict]) -> List[Task]:
        tasks: List[Task] = []
        for task_dict in tasks_dict:
            task_object: Task = get_db_object_from_dict(object_dict=task_dict, class_instance=Task)
            tasks.append(task_object)
        return tasks

    @staticmethod
    def count_amount_failed_task_in_timestamp(status_timestamp: List[StatusTimestamp]) -> int:
        counter = 0
        for timestamp in status_timestamp:
            if timestamp.status == TaskConsts.FAILED:
                counter += 1
        return counter
