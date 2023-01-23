from functools import cache

from server_logger.logger import ServerLogger


@cache
def get_current_logger(*args, **kwargs):
    """
    Singleton server_logger
    :return:
    """
    return ServerLogger(*args, **kwargs)


def is_method(args) -> bool:
    try:
        if args[0].__class__.__name__:
            return True
    except IndexError:
        return False


def log_function(func):
    server_logger = ServerLogger()

    def inner(*args, **kwargs):
        if is_method(args=args):
            server_logger.debug(f"{args[0].__class__.__name__} - {func.__name__} method started")
            res = func(*args, **kwargs)
            server_logger.debug(f"{args[0].__class__.__name__} - {func.__name__} method ended")
        else:
            server_logger.debug(f"{func.__name__} function started")
            res = func(*args, **kwargs)
            server_logger.debug(f"{func.__name__} function ended")
        return res

    return inner
