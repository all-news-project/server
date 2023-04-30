import os


class TaskConsts:
    TIMES_TRY_CREATE_TASK = int(os.getenv(key="TIMES_TRY_CREATE_TASK", default=3))
    TASKS_TABLE_NAME = "tasks"
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    SUCCEEDED = "succeeded"


class ArticleConsts:
    pass


class ClusterConsts:
    pass
