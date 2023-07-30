import os


class DBConsts:
    TASKS_TABLE_NAME = "tasks"
    ARTICLES_TABLE_NAME = "articles"
    CLUSTERS_TABLE_NAME = "clusters"
    GIT_DB_NAME = "git"
    GIT_DB_URL = "https://all-news-project.github.io/api-data/"
    GIT_DB_DELETE_ERROR_MSG = "Cannot delete using GitDBDriver"
    GIT_DB_INSERT_ERROR_MSG = "Cannot insert using GitDBDriver"
    GIT_DB_UPDATE_ERROR_MSG = "Cannot update using GitDBDriver"
    GIT_DB_COLLECTIONS = [ARTICLES_TABLE_NAME, CLUSTERS_TABLE_NAME]
    CLUSTER_LOW_SIM = int(os.getenv(key="CLUSTER_LOW_SIM", default=60))
    CLUSTER_HIGH_SIM = int(os.getenv(key="CLUSTER_HIGH_SIM", default=90))
    CLUSTER_THRESHOLD = int(os.getenv(key="CLUSTER_THRESHOLD", default=70))


class DBObjectsConsts:
    DATETIME_ATTRIBUTES = {
        DBConsts.ARTICLES_TABLE_NAME: ['collecting_time', 'publishing_time'],
        DBConsts.CLUSTERS_TABLE_NAME: ['creation_time', 'last_updated']
    }
