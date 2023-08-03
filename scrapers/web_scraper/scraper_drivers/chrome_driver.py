import os
import random
from datetime import datetime
from time import sleep
from typing import List

from selenium.common import InvalidArgumentException, NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options

from logger import get_current_logger, log_function
from scrapers.web_scraper.scraper_drivers.utils.driver_consts import BrowserConsts, MainConsts
from scrapers.web_scraper.scraper_drivers.interfaces.base_driver_interface import BaseDriverInterface
from scrapers.web_scraper.scraper_drivers.utils.driver_utils import get_driver_path, get_temp_browser_profile_path, \
    create_path_if_needed, kill_browser_childes
from selenium import webdriver

from scrapers.web_scraper.scraper_drivers.utils.element import Element


class ChromeDriver(BaseDriverInterface):
    SLEEP_AFTER_KILLING_CHILD_PROCESS = int(os.getenv(key="SLEEP_AFTER_KILLING_CHILD_PROCESS", default=10))

    def __init__(self, browser_type: str = BrowserConsts.CHROME, browser_profile_path: str = None,
                 webdriver_path: str = None, headless: bool = False, quit_at_end: bool = True):
        """
        Constructor
        :param browser_profile_path: a browser profile path
        :param webdriver_path: selenium web driver executable path
        :param headless: open the browser headless
        :param quit_at_end: exit browser after done
        """

        # Logger
        self.logger = get_current_logger()

        # Web driver path
        self.webdriver_path = webdriver_path if webdriver_path else get_driver_path(browser_type=browser_type)
        self.logger.debug(f"WebDriver path is: '{self.webdriver_path}'")

        # Browser profile path
        if browser_profile_path:
            self.browser_profile_path = browser_profile_path
        else:
            self.browser_profile_path = get_temp_browser_profile_path(browser_type=browser_type)
        create_path_if_needed(path=self.browser_profile_path)
        self.logger.debug(f"Browser profile path is: '{self.browser_profile_path}'")

        # Exit the window after the bot done
        self.teardown = quit_at_end

        # Headless
        self.headless = headless

        # Browser type
        self.browser_type = browser_type

        self.__init_chrome_driver__()

        # Implicitly wait time
        self._driver.implicitly_wait(MainConsts.IMPLICITLY_WAIT_TIME)

        # Page load timeout
        self._driver.set_page_load_timeout(MainConsts.DEFAULT_PAGE_LOAD_TIMEOUT)

        # Maximize the page window
        self._driver.maximize_window()

        self.logger.debug(f"Initialized {self.browser_type} web driver, headless: {self.headless}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        When the bot is done his running
        If teardown is True, exit
        Else, do not exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if self.teardown:
            self.exit()

    @log_function
    def __init_chrome_driver__(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(argument=f"user-data-dir={self.browser_profile_path}")
            if self.headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('start-maximized')
                chrome_options.add_argument('disable-infobars')
                chrome_options.add_argument("--disable-extensions")
            start_time = datetime.now()
            self._driver = webdriver.Chrome(executable_path=self.webdriver_path, options=chrome_options)
            end_time = datetime.now()
            self.logger.info(f"Init chrome driver in {(end_time - start_time).total_seconds()} seconds")
        except Exception as e:
            self.logger.error(f"Error initialize chrome driver - {str(e)}")
            if "executable needs to be in path" in str(e).lower():
                self.logger.error(f"PATH Error")
            if "chromedriver is assuming that chrome has crashed" in str(e).lower():
                kill_browser_childes(process_name=self.browser_type)
                self.logger.warning(f"Killed {self.browser_type} childes, run again")
                sleep(self.SLEEP_AFTER_KILLING_CHILD_PROCESS)
                return
            if "current browser version" in str(e).lower():
                self.logger.error(f"Error with browser version")
            raise e

    @log_function
    def exit(self):
        self._driver.quit()
        self.logger.info(f"Exit Chrome Driver")

    @log_function
    def get_url(self, url: str):
        for trie in range(MainConsts.GET_URL_TRIES):
            try:
                self.logger.debug(f"Trying to get page url: `{url}` NO. {trie + 1}/{MainConsts.GET_URL_TRIES}")
                self._driver.get(url)
                self.logger.info(f"Get to page url: `{url}`")
                return
            except InvalidArgumentException:
                desc = f"Error getting url: '{url}' - invalid url input format, please give full correct format"
                self.__error_and_exit(desc)
            except (WebDriverException, TimeoutException) as e:
                if "ERR_CONNECTION_RESET" in str(e):
                    continue
                desc = f"Error getting to page url: `{url}` - {str(e)}"
                self.__error_and_exit(desc)
            except Exception as e:
                desc = f"Error getting to page url: `{url}` - {str(e)}"
                self.__error_and_exit(desc)
        self.__error_and_exit(f"Error getting to page url: `{url}` after {MainConsts.GET_URL_TRIES} tries")

    @log_function
    def __error_and_exit(self, desc):
        self.logger.error(desc)
        self.exit()

    @log_function
    def get_current_url(self) -> str:
        return self._driver.current_url if self._driver.current_url not in BrowserConsts.NEW_TAB_URLS else None

    @log_function
    def get_title(self) -> str:
        return self._driver.title if self._driver.title != BrowserConsts.NEW_TAB_TITLE and self._driver.title else None

    @log_function
    def find_element(self, by, value) -> Element:
        real_element = self._driver.find_element(by=by, value=value)
        element_text = real_element.text
        return Element(read_element=real_element, text=element_text)

    @log_function
    def find_elements(self, by, value) -> List[Element]:
        try:
            elements: List[Element] = []
            real_elements = self._driver.find_elements(by=by, value=value)
            for real_element in real_elements:
                element = Element(read_element=real_element, text=real_element.text)
                elements.append(element)
            return elements
        except StaleElementReferenceException:
            return []

    @log_function
    def is_element_appears(self, by, value, timeout: int = 0) -> bool:
        try:
            self.wait_until_object_appears(by=by, value=value, timeout=timeout)
            return True
        except TimeoutException:
            return False
        except Exception as e:
            self.logger.error(f"Error while check if element is appears - {str(e)}")
            raise e

    @log_function
    def wait_until_object_appears(self, by, value, timeout: int = MainConsts.DEFAULT_ELEMENT_TIMEOUT):
        start_time = datetime.now()
        seconds_pass = 0
        seconds_counter = 0
        while seconds_pass < timeout:
            seconds_pass = (datetime.now() - start_time).total_seconds()
            try:
                if seconds_pass > seconds_counter + 1:
                    self.logger.debug(f"Waiting for element `{value}` to appears timeout: {seconds_pass:.3f}/{timeout}")
                elements = self._driver.find_elements(by=by, value=value)
                if not elements:
                    raise NoSuchElementException
                self.logger.info(f"Element {value} found")
                return
            except NoSuchElementException:
                seconds_counter = int(seconds_pass)
                sleep(MainConsts.ELEMENT_SLEEPING_TIME)
                continue
        raise TimeoutException

    @log_function
    def insert_text(self, by, value, text: str, press_enter_needed: bool = True):
        try:
            self.click_on_element(by=by, value=value)
            for char in text:
                self.key_press(char)
            self.logger.info(f"Text: '{text}' inserted to element")
            if press_enter_needed:
                self.key_press(Keys.ENTER)
                self.logger.info("Enter key pressed")
        except Exception as e:
            self.logger.error(f"Error while trying to insert text: '{text}' to element: '{value}' - {str(e)}")
            raise e

    @log_function
    def move_to_element(self, by, value):
        try:
            action = webdriver.ActionChains(self._driver)
            element = self._driver.find_element(by=by, value=value)
            action.move_to_element(element)
            action.perform()
            self.logger.info(f"Moved to element")
        except Exception as e:
            exception_desc = str(e).split('\n')[0] if str(e) else ''
            self.logger.warning(f"Error while trying to move to element - {exception_desc}")

    @log_function
    def click_on_element(self, by, value):
        try:
            self.move_to_element(by=by, value=value)
            action = webdriver.ActionChains(self._driver)
            action.click()
            action.perform()
            self.logger.info(f"Element clicked")
        except Exception as e:
            self.logger.error(f"Error while trying to click element - {str(e)}")
            raise e

    @log_function
    def is_input_cleared(self, by, value) -> bool:
        return self.find_element(by=by, value=value).get_attribute("value") == ""

    @log_function
    def clear_input(self, by, value, timeout: int = MainConsts.CLEAR_ELEMENT_TEXT_TIMEOUT):
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            if self.is_input_cleared(by=by, value=value):
                self.logger.info(f"Element is cleared")
                return
            self.click_on_element(by=by, value=value)
            self.multiple_key_press(keys_to_press=[Keys.CONTROL, 'a'])
            self.key_press(key_to_press=Keys.BACKSPACE)
        self.logger.warning(f"Error clearing element after {MainConsts.CLEAR_ELEMENT_TEXT_TIMEOUT} timeout")

    def multiple_key_press(self, keys_to_press: List[str]):
        for key_to_press in keys_to_press:
            ActionChains(self._driver).key_down(key_to_press).perform()
            sleep(MainConsts.INSERT_TEXT_SLEEPING_TIME)

        random.shuffle(keys_to_press)
        for key_to_press in keys_to_press:
            ActionChains(self._driver).key_up(key_to_press).perform()
            sleep(MainConsts.INSERT_TEXT_SLEEPING_TIME)

    def key_press(self, key_to_press: str):
        ActionChains(self._driver).key_down(key_to_press).key_up(key_to_press).perform()
        sleep(MainConsts.INSERT_TEXT_SLEEPING_TIME)
