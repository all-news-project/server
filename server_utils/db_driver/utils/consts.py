class DBConsts:
    TASKS_TABLE_NAME = "tasks"
    ARTICLE_TABLE_NAME = "articles"
    CLUSTERS_TABLE_NAME = "clusters"
    GIT_DB_NAME = "git"
    GIT_DB_URL = "https://all-news-project.github.io/api-data/"
    GIT_DB_DELETE_ERROR_MSG = "Cannot delete using GitDBDriver"
    GIT_DB_INSERT_ERROR_MSG = "Cannot insert using GitDBDriver"
    GIT_DB_UPDATE_ERROR_MSG = "Cannot update using GitDBDriver"
    GIT_DB_COLLECTIONS = [ARTICLE_TABLE_NAME, CLUSTERS_TABLE_NAME]


class DBObjectsConsts:
    DATETIME_ATTRIBUTES = {
        DBConsts.ARTICLE_TABLE_NAME: ['collecting_time', 'publishing_time'],
        DBConsts.CLUSTERS_TABLE_NAME: ['creation_time', 'last_updated']
    }
