from typing import Union

from bs4 import Tag
from lxml.etree import _Element  # todo: change to ElementBase?
from selenium.webdriver.remote.webelement import WebElement

from scrapers.scraper_drivers.interfaces.element_interface import ElementInterface
from scrapers.scraper_drivers.utils.driver_consts import ElementsConsts
from scrapers.scraper_drivers.utils.exceptions import UnknownElementTypeException
from server_utils import get_current_logger, log_function


class Element(ElementInterface):
    def __init__(self, read_element: Union[Tag, WebElement, _Element], text: str = None):
        self.logger = get_current_logger()
        self.real_element = read_element
        self.__set_element_type()
        self.text = text

    def set_text(self, text: str):
        self.text = text

    def __set_element_type(self):
        if isinstance(self.real_element, Tag):
            self.element_type = ElementsConsts.REQ_ELEMENT
        elif isinstance(self.real_element, WebElement):
            self.element_type = ElementsConsts.WEB_ELEMENT
        elif isinstance(self.real_element, _Element):
            self.element_type = ElementsConsts.XML_ELEMENT
        else:
            self.__raise_unknown_element_exception()

    @log_function
    def __raise_unknown_element_exception(self):
        desc = f"Unknown Element Type: `{type(self.real_element)}`"
        self.logger.error(desc)
        raise UnknownElementTypeException(desc)

    @log_function
    def get_text(self) -> str:
        return self.text if self.text is not None else self.real_element.text

    @log_function
    def get_tag_name(self) -> str:
        if self.element_type == ElementsConsts.WEB_ELEMENT:
            return self.real_element.tag_name
        elif self.element_type == ElementsConsts.REQ_ELEMENT:
            return self.real_element.name
        elif self.element_type == ElementsConsts.XML_ELEMENT:
            return self.real_element.tag
        else:
            self.__raise_unknown_element_exception()

    @log_function
    def get_attribute(self, attribute: str) -> str:
        if self.element_type == ElementsConsts.WEB_ELEMENT:
            return self.real_element.get_attribute(attribute)
        elif self.element_type == ElementsConsts.REQ_ELEMENT:
            return self.real_element.attrs.get(attribute)
        elif self.element_type == ElementsConsts.XML_ELEMENT:
            return self.real_element.attrib.get(attribute)
        else:
            self.__raise_unknown_element_exception()

    @log_function
    def is_hidden(self) -> bool:
        if self.element_type == ElementsConsts.WEB_ELEMENT:
            return not self.real_element.is_displayed()
        elif self.element_type == ElementsConsts.REQ_ELEMENT:
            return self.real_element.hidden
        elif self.element_type == ElementsConsts.XML_ELEMENT:
            return False  # todo: check if there is a way to check if hidden
        else:
            self.__raise_unknown_element_exception()
