import logging
import os
import sys

from logger.formatters.color_formatter import ColorFormatter
from logger.formatters.consts import MainConsts
from logger.handlers.log_db_handler import LogDBHandler
from server_utils.singleton_class import Singleton


def check_last_log(func):
    def inner(*args, **kwargs):
        msg = get_message_from_log_args(*args, **kwargs)
        log_data = {
            "level": func.__name__.upper(),
            "msg": msg,
            "task_id": args[0].task_id,
            "task_type": args[0].task_type
        }
        last_log = args[0].last_log

        if last_log != log_data:
            func(*args, **kwargs)
            args[0].set_last_log(log_data)

    return inner


def get_message_from_log_args(*args, **kwargs) -> str:
    if len(args) > 1:
        msg = args[1]
    elif kwargs.get("msg"):
        msg = kwargs.get("msg")
    else:
        msg = ""
    return msg


class ServerLogger(Singleton):
    SAVE_LOG_TO_DB = bool(os.getenv(key="SAVE_LOG_TO_DB", default=False))
    __initialized = False

    def __init__(self, task_id: str = None, task_type: str = None):
        root_logger = logging.getLogger()
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_format = MainConsts.CONSOLE_FORMAT
        colored_formatter = ColorFormatter(console_format)
        console_handler.setFormatter(colored_formatter)

        self.logger = logging.getLogger("server_logger")
        self.logger.setLevel(level=logging.DEBUG)

        self.__task_id = task_id
        if self.__task_id or not hasattr(self.logger, "task_id"):
            self.logger.__setattr__("task_id", self.__task_id)

        self.__task_type = task_type
        if self.__task_type or not hasattr(self.logger, "task_type"):
            self.logger.__setattr__("task_type", self.__task_type)

        if not self.__initialized:
            root_logger.addHandler(console_handler)
            self.add_db_handler()
            self.__initialized = True

        self.__last_log = dict()

    @property
    def task_id(self):
        return self.__task_id

    @property
    def task_type(self):
        return self.__task_type

    @property
    def last_log(self):
        return self.__last_log

    def set_last_log(self, log: dict):
        self.__last_log = log

    def add_db_handler(self):
        if self.SAVE_LOG_TO_DB:
            db_handler = LogDBHandler()
            db_handler.setLevel(self.logger.getEffectiveLevel())
            self.logger.addHandler(db_handler)

    @check_last_log
    def debug(self, msg: str):
        self.logger.debug(msg=msg, extra=self._prepare_msg_extra())

    @check_last_log
    def info(self, msg: str):
        self.logger.info(msg=msg, extra=self._prepare_msg_extra())

    @check_last_log
    def warning(self, msg: str):
        self.logger.warning(msg=msg, extra=self._prepare_msg_extra())

    @check_last_log
    def error(self, msg: str):
        self.logger.error(msg=msg, extra=self._prepare_msg_extra())

    @check_last_log
    def exception(self, msg: str):
        self.logger.critical(msg=msg, extra=self._prepare_msg_extra())

    def _prepare_msg_extra(self):
        extra = dict()
        if hasattr(self.logger, "task_id"):
            extra["task_id"] = self.logger.task_id

        if hasattr(self.logger, "task_type"):
            extra["task_type"] = self.logger.task_type

        return extra
