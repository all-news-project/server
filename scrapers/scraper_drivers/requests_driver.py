import requests
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from server_utils.logger import get_current_logger, log_function
from scrapers.scraper_drivers.utils.driver_consts import MainConsts
from scrapers.scraper_drivers.utils.element import Element
from scrapers.scraper_drivers.utils.exceptions import PageNotFoundException, AttributeNameException
from scrapers.scraper_drivers.interfaces.base_driver_interface import BaseDriverInterface

from urllib.request import urlopen
from lxml import etree

from typing import List


class RequestsDriver(BaseDriverInterface):
    def __init__(self, headless: bool = False):
        self.logger = get_current_logger()
        self.url = None
        self._current_soup_page = None
        self.headless = headless

    @log_function
    def exit(self):
        self.url = None
        self._current_soup_page = None
        self.logger.info(f"Exit Request Driver")

    @log_function
    def _get_page_tag_names(self) -> List[str]:
        return list({tag.name for tag in self._current_soup_page.findAll()})

    @log_function
    def get_url(self, url: str):
        try:
            for trie in range(MainConsts.GET_URL_TRIES):
                self.logger.debug(f"Trying to get page url: `{url}` NO. {trie + 1}/{MainConsts.GET_URL_TRIES}")
                page_res = requests.get(url, timeout=MainConsts.REQUEST_TIMEOUT)
                if page_res.status_code == 200:
                    self._current_soup_page = BeautifulSoup(page_res.text, 'html.parser')
                    self.url = page_res.url
                    self.logger.info(f"Get to page url: `{url}`")
                    return
            raise PageNotFoundException(f"Error getting page url: `{self.url}` after {MainConsts.GET_URL_TRIES} tries")
        except Exception as e:
            desc = f"Error getting url: `{url}` - `{e}`"
            self.logger.error(desc)
            raise PageNotFoundException(desc)

    @log_function
    def get_current_url(self) -> str:
        return self.url

    @log_function
    def get_title(self) -> str:
        return self._current_soup_page.title.text if self._current_soup_page else None

    @log_function
    def find_element(self, by, value) -> Element:
        element = None
        try:
            if by == By.ID:
                element = self._current_soup_page.find(attrs={"id": value})
            elif by == By.CLASS_NAME:
                element = self._current_soup_page.find(attrs={"class": value})
            elif by == By.XPATH:
                htmlparser = etree.HTMLParser()
                response = urlopen(self.url)
                tree = etree.parse(response, htmlparser)
                element = tree.xpath(value)[0]
            else:
                raise AttributeNameException(f"Cannot find element by: `{by}`")
        except Exception as e:
            self.__raise_no_such_element_exception(by=by, value=value, exception=e)
        if element is None:
            self.__raise_no_such_element_exception(by=by, value=value, exception=NoSuchElementException)
        return Element(read_element=element, text=element.text)

    def __raise_no_such_element_exception(self, by, value, exception):
        desc = f"Cannot find element by: `{by}` with value: `{value}` - {str(exception)}"
        self.logger.error(desc)
        raise NoSuchElementException(desc)

    @log_function
    def find_elements(self, by, value) -> List[Element]:
        elements = None
        try:
            if by == By.ID:
                elements = self._current_soup_page.findAll(attrs={"id": value})
            elif by == By.CLASS_NAME:
                elements = self._current_soup_page.findAll(attrs={"class": value})
            elif by == By.XPATH:
                htmlparser = etree.HTMLParser()
                response = urlopen(self.url)
                tree = etree.parse(response, htmlparser)
                elements = tree.xpath(value)
            else:
                raise AttributeNameException(f"Cannot find element by: `{by}`")
        except Exception as e:
            self.__raise_no_such_element_exception(by=by, value=value, exception=e)
        if elements is None:
            return list()
        return [Element(read_element=element, text=element.text) for element in elements]
