from datetime import datetime
from time import sleep

from selenium.common import InvalidArgumentException, NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys

from logger import get_current_logger, log_function
from scrapers.scraper_component.utils.driver_consts import BrowserConsts, MainConsts
from scrapers.scraper_component.interfaces.base_driver_interface import BaseDriverInterface
from scrapers.scraper_component.utils.driver_utils import get_driver_path, get_temp_browser_profile_path, \
    create_path_if_needed, kill_browser_childes
from selenium import webdriver


class ChromeDriver(BaseDriverInterface):
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
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(argument=f"user-data-dir={self.browser_profile_path}")
            self._driver = webdriver.Chrome(executable_path=self.webdriver_path, options=options)
        except Exception as e:
            if "executable needs to be in path" in str(e).lower():
                self.logger.error(f"PATH Error")
            self.logger.error(f"Error initialize chrome driver - {str(e)}")
            if "chromedriver is assuming that chrome has crashed" in str(e).lower():
                kill_browser_childes(process_name=self.browser_type)
                self.logger.warning(f"Killed {self.browser_type} childes, run again")
                return
            raise e

    @log_function
    def exit(self):
        self._driver.quit()
        self.logger.info(f"ChromeDriver exit")

    @log_function
    def get_url(self, url: str):
        try:
            self._driver.get(url)
        except InvalidArgumentException:
            self.logger.error(f"Error getting url: '{url}' - invalid url input format, please give full correct format")
            self.exit()

    @log_function
    def get_current_url(self) -> str:
        return self._driver.current_url

    @log_function
    def get_title(self) -> str:
        return self._driver.title

    @log_function
    def find_element(self, by, value):
        return self._driver.find_element(by=by, value=value)

    @log_function
    def find_elements(self, by, value):
        return self._driver.find_elements(by=by, value=value)

    @log_function
    def wait_until_object_appears(self, by, value, timeout: int = MainConsts.DEFAULT_ELEMENT_TIMEOUT):
        start_time = datetime.now()
        seconds_pass = 0
        while seconds_pass < timeout:
            seconds_pass = (datetime.now() - start_time).total_seconds()
            try:
                self.logger.debug(f"Waiting for element {value} to appears TIMEOUT: ({seconds_pass}/{timeout})")
                elements = self._driver.find_elements(by=by, value=value)
                if not elements:
                    raise NoSuchElementException
                self.logger.info(f"Element {value} found")
                return
            except NoSuchElementException:
                sleep(MainConsts.ELEMENT_SLEEPING_TIME)
                continue
        raise TimeoutException

    @log_function
    def insert_text(self, by, value, text: str, press_enter_needed: bool = True):
        try:
            self.click_on_element(by=by, value=value)
            for char in text:
                ActionChains(self._driver).key_down(char).key_up(char).perform()
                sleep(MainConsts.INSERT_TEXT_SLEEPING_TIME)
            self.logger.info(f"Text: '{text}' inserted to element")
            if press_enter_needed:
                ActionChains(self._driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
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
            self.logger.error(f"Error while trying to move to element - {str(e)}")

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
