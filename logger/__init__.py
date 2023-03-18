from functools import cache

from logger.wise_logger import WISELogger


@cache
def get_current_logger(*args, **kwargs):
    """
    Singleton logger
    :return:
    """
    return WISELogger(*args, **kwargs)


def is_method(args) -> bool:
    try:
        if args[0].__class__.__name__:
            return True
    except IndexError:
        return False


def log_function(func):
    logger = WISELogger()

    def inner(*args, **kwargs):
        if is_method(args=args):
            logger.debug(f"{args[0].__class__.__name__} - {func.__name__} method started")
            res = func(*args, **kwargs)
            logger.debug(f"{args[0].__class__.__name__} - {func.__name__} method ended")
        else:
            logger.debug(f"{func.__name__} function started")
            res = func(*args, **kwargs)
            logger.debug(f"{func.__name__} function ended")
        return res

    return inner
