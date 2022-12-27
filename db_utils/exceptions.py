class DataNotFoundException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class InsertDataException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
