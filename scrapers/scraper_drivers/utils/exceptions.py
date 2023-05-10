class PageNotFoundException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnknownWebDriverException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnknownOperatingSystemException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnknownBrowserException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnknownElementTypeException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class AttributeNameException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class ErrorClickElementException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
