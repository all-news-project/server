from db_driver import get_current_db_driver
from db_driver.db_objects.cluster import Cluster
from db_driver.db_objects.db_objects_utils import get_db_object_from_dict
from db_driver.utils.consts import DBConsts
# from logger import get_current_logger


class ClusterUtils:
    def __init__(self):
        # self.logger = get_current_logger()
        self._db = get_current_db_driver()

    def get_cluster(self, cluster_id: str) -> Cluster:
        data_filter = {"cluster_id": cluster_id}
        cluster_data = self._db.get_one(table_name=DBConsts.CLUSTERS_TABLE_NAME, data_filter=data_filter)
        cluster_object: Cluster = get_db_object_from_dict(object_dict=cluster_data, class_instance=Cluster)
        return cluster_object
