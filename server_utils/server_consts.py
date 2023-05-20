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
    TIMES_TRY_INSERT_ARTICLE = int(os.getenv(key="TIMES_TRY_INSERT_ARTICLE", default=3))
    TIMES_TRY_UPDATE_CLUSTER_ID = int(os.getenv(key="TIMES_TRY_UPDATE_CLUSTER_ID", default=3))


class ClusterConsts:
    TIMES_TRY_INSERT_CLUSTER = int(os.getenv(key="TIMES_TRY_INSERT_ARTICLE", default=3))
    TIMES_TRY_UPDATE_CLUSTER = int(os.getenv(key="TIMES_TRY_UPDATE_CLUSTER_ID", default=3))
