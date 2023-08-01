from scrapers.web_scraper.scraper_drivers.utils.driver_consts import MainConsts


class BaseDriverInterface:
    def wait_until_object_appears(self, by, value, timeout: int = MainConsts.DEFAULT_ELEMENT_TIMEOUT):
        raise NotImplementedError

    def insert_text(self, by, value, text: str, press_enter_needed: bool = True):
        raise NotImplementedError

    def move_to_element(self, by, value):
        raise NotImplementedError

    def click_on_element(self, by, value):
        raise NotImplementedError
