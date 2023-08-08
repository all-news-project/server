class UnknownWebsiteScraperException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class FailedGetURLException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnwantedArticleException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class FailedGetArticleException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class FailedConstantlyArticleException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
