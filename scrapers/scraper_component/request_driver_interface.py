class RequestDriverInterface:
    def get_url(self, url: str):
        raise NotImplementedError

    def get_current_url(self) -> str:
        raise NotImplementedError

    def get_title(self) -> str:
        raise NotImplementedError

    def find_element(self, by, value, tag_name: str = None):
        raise NotImplementedError
