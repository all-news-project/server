import logging
import os
import sys
from functools import cache

from logger.formatters.color_formatter import ColorFormatter
from logger.formatters.consts import MainConsts
from logger.log_db_handler import LogDBHandler


@cache
class ServerLogger:
    SAVE_LOG_TO_DB = bool(os.getenv(key="SAVE_LOG_TO_DB", default=False))

    def __init__(self, task_id: str = None, task_type: str = None):
        root_logger = logging.getLogger()
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_format = MainConsts.CONSOLE_FORMAT
        colored_formatter = ColorFormatter(console_format)
        console_handler.setFormatter(colored_formatter)
        root_logger.addHandler(console_handler)
        self.logger = logging.getLogger("server_logger")
        self.logger.setLevel(level=logging.DEBUG)

        if task_id or not hasattr(self.logger, "task_id"):
            self.logger.__setattr__("task_id", task_id)

        if task_type or not hasattr(self.logger, "task_type"):
            self.logger.__setattr__("task_type", task_type)

        self.add_db_handler()

    def add_db_handler(self):
        if self.SAVE_LOG_TO_DB:
            db_handler = LogDBHandler()
            db_handler.setLevel(self.logger.getEffectiveLevel())
            self.logger.addHandler(db_handler)

    def debug(self, msg: str):
        self.logger.debug(msg=msg, extra=self._prepare_msg_extra())

    def info(self, msg: str):
        self.logger.info(msg=msg, extra=self._prepare_msg_extra())

    def warning(self, msg: str):
        self.logger.warning(msg=msg, extra=self._prepare_msg_extra())

    def error(self, msg: str):
        self.logger.error(msg=msg, extra=self._prepare_msg_extra())

    def exception(self, msg: str):
        self.logger.critical(msg=msg, extra=self._prepare_msg_extra())

    def _prepare_msg_extra(self):
        extra = dict()
        if hasattr(self.logger, "task_id"):
            extra["task_id"] = self.logger.task_id

        if hasattr(self.logger, "task_type"):
            extra["task_type"] = self.logger.task_type

        return extra
