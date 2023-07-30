class MainConsts:
    SERVER_LOGGER_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s | %(task_type)s | %(task_id)s"
    LOGGER_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
    LEVEL_FIELDS = ["levelname", "levelno"]


class ColorCodes:
    GREY = "\x1b[38;21m"
    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[1;33m"
    RED = "\x1b[1;31m"
    BOLD_RED = "\x1b[0;35m"
    BLUE = "\x1b[1;34m"
    LIGHT_BLUE = "\x1b[1;36m"
    PURPLE = "\x1b[1;35m"
    RESET = "\x1b[0m"
