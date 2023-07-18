from datetime import datetime
from unittest import TestCase
from uuid import uuid4

from db_driver import get_current_db_driver
from server_utils.db_driver.db_objects import get_db_object_from_dict
from logger import get_current_logger
from server_utils.logger.objects.log import Log


class TestServerLoggerDB(TestCase):
    def test_debug(self):
        task_id = str(uuid4())
        task_type = "text_debug"
        msg = "text_debug_" * 10
        level = "DEBUG"

        logger = get_current_logger(task_id=task_id, task_type=task_type)
        db = get_current_db_driver()

        self.assertEqual(logger, db.logger)

        all_log_args = {"table_name": "log", "data_filter": {"task_type": task_type}}
        db.delete_many(**all_log_args)

        is_exists_by_task_id = db.count(**all_log_args)
        self.assertEqual(is_exists_by_task_id, 4)

        self.assertIsNotNone(logger)
        current_time = datetime.now()
        logger.debug(msg=msg)

        log_args = {"table_name": "log", "data_filter": {"task_id": task_id, "msg": msg}}
        is_exists_by_task_id = db.exists(**log_args)
        self.assertTrue(is_exists_by_task_id)

        log_count = db.count(**log_args)
        self.assertTrue(log_count > 0)

        logger_db_object = db.get_one(**log_args)
        log_object: Log = get_db_object_from_dict(object_dict=logger_db_object, class_instance=Log)

        self.assertEqual(task_id, log_object.task_id)
        self.assertEqual(task_type, log_object.task_type)
        self.assertEqual(msg, log_object.msg)
        self.assertEqual(level, log_object.level)

        log_time = log_object.created
        seconds_pass = (current_time - log_time).total_seconds()
        self.assertTrue(seconds_pass < 10)

        deleted = db.delete_many(**log_args)
        self.assertTrue(deleted)

        is_exists_by_task_id = db.exists(**log_args)
        self.assertFalse(is_exists_by_task_id)

        log_count = db.count(**log_args)
        self.assertEqual(log_count, 0)

        db.delete_many(**all_log_args)

    def test_info(self):
        self.fail()

    def test_warning(self):
        self.fail()

    def test_error(self):
        self.fail()

    def test_exception(self):
        self.fail()
