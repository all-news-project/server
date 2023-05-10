import os


class ScheduleConsts:
    SLEEPING_TIME = int(os.getenv(key="SLEEPING_TIME", default=60 * 15))


class TaskConsts:
    TIMES_TRY_CREATE_TASK = int(os.getenv(key="TIMES_TRY_CREATE_TASK", default=3))
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    SUCCEEDED = "succeeded"
    UNWANTED = "unwanted"


class ArticleConsts:
    pass


class ClusterConsts:
    pass
