from server_logger import log_function, get_current_logger, ServerLogger


@log_function
def dummy_function(logger: ServerLogger):
    logger.warning("inner dummy_function")


class DummyClass:
    def __init__(self):
        self.logger = ServerLogger()

    @log_function
    def dummy_method(self):
        self.logger.warning(f"inner dummy_method")


if __name__ == '__main__':
    server_logger = get_current_logger()
    server_logger.debug("message debug message")
    server_logger.info("message info message")
    server_logger.warning("message warning message")
    server_logger.error("message error message")
    server_logger.exception("message exception message")
    dummy_function(logger=server_logger)
    dummy_class = DummyClass()
    dummy_class.dummy_method()
