import os


class DBConsts:
    TASKS_TABLE_NAME = "tasks"
    ARTICLES_TABLE_NAME = "articles"
    CLUSTERS_TABLE_NAME = "clusters"
    CLUSTER_LOW_SIM = int(os.getenv(key="CLUSTER_LOW_SIM", default=60))
    CLUSTER_HIGH_SIM = int(os.getenv(key="CLUSTER_HIGH_SIM", default=90))
    CLUSTER_THRESHOLD = int(os.getenv(key="CLUSTER_THRESHOLD", default=70))
