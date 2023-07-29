class DataNotFoundDBException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class InsertDataDBException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class DeleteDataDBException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UpdateDataDBException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class ErrorConnectDBException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
