class ElementInterface:
    def get_text(self) -> str:
        raise NotImplementedError

    def get_tag_name(self) -> str:
        raise NotImplementedError

    def get_attribute(self, attribute: str) -> str:
        raise NotImplementedError

    def is_hidden(self) -> bool:
        raise NotImplementedError
