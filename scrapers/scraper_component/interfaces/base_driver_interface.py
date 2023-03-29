from typing import List

from scrapers.scraper_component.utils.element import Element


class BaseDriverInterface:
    def get_url(self, url: str):
        raise NotImplementedError

    def get_current_url(self) -> str:
        raise NotImplementedError

    def get_title(self) -> str:
        raise NotImplementedError

    def find_element(self, by, value) -> Element:
        raise NotImplementedError

    def find_elements(self, by, value) -> List[Element]:
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError
