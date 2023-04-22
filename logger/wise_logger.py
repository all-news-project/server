import logging
import sys
from functools import cache

from logger.color_formatter import ColorFormatter
from logger.consts import MainConsts


@cache
class WISELogger:

    def __init__(self):
        root_logger = logging.getLogger()
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_format = MainConsts.CONSOLE_FORMAT
        colored_formatter = ColorFormatter(console_format)
        console_handler.setFormatter(colored_formatter)
        root_logger.addHandler(console_handler)
        self.logger = logging.getLogger("wise_logger")
        self.logger.setLevel(level=logging.DEBUG)

    def debug(self, msg: str):
        self.logger.debug(msg=msg)

    def info(self, msg: str):
        self.logger.info(msg=msg)

    def warning(self, msg: str):
        self.logger.warning(msg=msg)

    def error(self, msg: str):
        self.logger.error(msg=msg)

    def exception(self, msg: str):
        self.logger.critical(msg=msg)