from datetime import datetime
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
