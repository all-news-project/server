import os


class ScheduleConsts:
    SLEEPING_TIME = int(os.getenv(key="SLEEPING_TIME", default=60 * 15))


class TaskConsts:
    MAX_TIME_FAILED = int(os.getenv(key="MAX_TIME_FAILED", default=10))
    DESC_UNWANTED = "Task is unwanted"
    DESC_SUCCEEDED = "Task succeeded"
    TIMES_TRY_CREATE_TASK = int(os.getenv(key="TIMES_TRY_CREATE_TASK", default=3))
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    FAILED_CONSTANTLY = "failed_constantly"
    FAILED_GET_URL = "failed_get_url"
    SUCCEEDED = "succeeded"
    UNWANTED = "unwanted"


class ArticleConsts:
    TIMES_TRY_INSERT_ARTICLE = int(os.getenv(key="TIMES_TRY_INSERT_ARTICLE", default=3))
    TIMES_TRY_UPDATE_CLUSTER_ID = int(os.getenv(key="TIMES_TRY_UPDATE_CLUSTER_ID", default=3))


class ClusterConsts:
    TIMES_TRY_INSERT_CLUSTER = int(os.getenv(key="TIMES_TRY_INSERT_ARTICLE", default=3))
    TIMES_TRY_UPDATE_CLUSTER = int(os.getenv(key="TIMES_TRY_UPDATE_CLUSTER_ID", default=3))
