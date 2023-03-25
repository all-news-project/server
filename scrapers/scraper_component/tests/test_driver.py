from time import sleep
from unittest import TestCase

from selenium.webdriver.common.by import By

from scrapers.scraper_component import get_scraping_driver
from scrapers.scraper_component.utils.driver_consts import BrowserConsts


class TestChromeDriver(TestCase):
    use_request_driver = False

    def test_get_current_url(self):
        url = "https://kggold4.github.io/todo-js-app/"
        driver = get_scraping_driver(via_request=self.use_request_driver)
        self.assertEqual(driver.get_current_url(), BrowserConsts.NEW_TAB_URL)
        driver.get_url(url=url)
        self.assertEqual(driver.get_current_url(), url)
        driver.exit()
        sleep(3)

    def test_get_title(self):
        url = "https://kggold4.github.io/todo-js-app/"
        title = "To Do App"
        driver = get_scraping_driver(via_request=self.use_request_driver)
        self.assertEqual(driver.get_title(), BrowserConsts.NEW_TAB_TITLE)
        driver.get_url(url=url)
        self.assertEqual(driver.get_title(), title)
        driver.exit()
        sleep(3)

    def test_find_element(self):
        url = "https://kggold4.github.io/todo-js-app/"
        driver = get_scraping_driver(via_request=self.use_request_driver)
        driver.get_url(url=url)

        # element 1
        element_1 = driver.find_element(by=By.ID, value="insertbtn")
        self.assertNotEqual(element_1, None)
        self.assertEqual(element_1.aria_role, "button")
        self.assertEqual(element_1.tag_name, "input")

        # element 2
        element_2 = driver.find_element(by=By.CLASS_NAME, value="tasksoutput")
        self.assertNotEqual(element_2, None)
        self.assertEqual(element_2.aria_role, "generic")
        self.assertEqual(element_2.tag_name, "span")

        # element 3
        element_3 = driver.find_element(by=By.XPATH, value="//h2[contains(text(), 'To Do App')]")
        self.assertNotEqual(element_3, None)
        self.assertEqual(element_3.aria_role, "heading")
        self.assertEqual(element_3.tag_name, "h2")
        self.assertEqual(element_3.text, "To Do App")
        driver.exit()
        sleep(3)

    def test_find_elements(self):
        url = "https://www.bbc.com/"
        driver = get_scraping_driver(via_request=self.use_request_driver)
        driver.get_url(url=url)
        elements_xpath = "//li[contains(@class, 'media-list__item media-list__item--')]"
        elements = driver.find_elements(by=By.XPATH, value=elements_xpath)
        self.assertTrue(len(elements) > 30)
        driver.exit()
        sleep(3)
