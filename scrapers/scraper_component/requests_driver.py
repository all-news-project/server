import requests
from bs4 import BeautifulSoup

from logger import get_current_logger
from scrapers.scraper_component.utils.exceptions import PageNotFoundException
from scrapers.scraper_component.interfaces.base_driver_interface import BaseDriverInterface

from typing import List


class RequestsDriver(BaseDriverInterface):
    def __init__(self):
        self.logger = get_current_logger()
        self.url = None
        self._current_soup_page = None

    def _get_page_tag_names(self) -> List[str]:
        return list({tag.name for tag in self._current_soup_page.findAll()})

    def get_url(self, url: str):
        try:
            page_res = requests.get(url)
            self._current_soup_page = BeautifulSoup(page_res.text, 'html.parser')
            self.url = page_res.url
            self.logger.info(f"Get to page url: `{self.url}`")
        except Exception as e:
            desc = f"Error getting url: `{url}` - `{e}`"
            self.logger.error(desc)
            raise PageNotFoundException(desc)

    def get_current_url(self) -> str:
        return self.url

    def get_title(self) -> str:
        return self._current_soup_page.title.text

    def find_element(self, by, value):
        # return self._current_soup_page.find(name=tag_name, attrs={by: value})
        pass

    def find_elements(self, by, value):
        pass


if __name__ == '__main__':
    rd = RequestsDriver()
    rd.get_url("https://www.bbc.com/")
    element = rd.find_element(by="class", value="block-link__overlay-link")
    print(element)
