from time import sleep
from unittest import TestCase

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from scrapers.web_scraper.scraper_drivers import get_scraping_driver


class TestChromeDriver(TestCase):
    # TODO: add tests that insert data to the database
    SLEEP_TIME_AFTER_TEST = 3
    USE_REQUEST_DRIVER = False
    HEADLESS = False

    def test_get_current_url(self):
        url = "https://kggold4.github.io/todo-js-app/"
        driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        self.assertIsNone(driver.get_current_url())
        driver.get_url(url=url)
        self.assertEqual(driver.get_current_url(), url)
        driver.exit()
        sleep(self.SLEEP_TIME_AFTER_TEST)

    def test_get_title(self):
        url = "https://kggold4.github.io/todo-js-app/"
        title = "To Do App"
        driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        self.assertIsNone(driver.get_title())
        driver.get_url(url=url)
        self.assertEqual(driver.get_title(), title)
        driver.exit()
        sleep(self.SLEEP_TIME_AFTER_TEST)

    def test_find_element(self):
        url = "https://kggold4.github.io/todo-js-app/"
        driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        driver.get_url(url=url)

        # element 1
        element_1 = driver.find_element(by=By.ID, value="insertbtn")
        self.assertIsNotNone(element_1)
        self.assertEqual(element_1.get_attribute("type"), "button")
        self.assertEqual(element_1.get_tag_name(), "input")
        self.assertFalse(element_1.is_hidden())
        self.assertEqual(element_1.get_text(), "")

        # element 2
        element_2 = driver.find_element(by=By.CLASS_NAME, value="tasksoutput")
        self.assertIsNotNone(element_2)
        self.assertEqual(element_1.get_text(), "")
        self.assertEqual(element_2.get_tag_name(), "span")

        # element 3
        element_3 = driver.find_element(by=By.XPATH, value="//h2[contains(text(), 'To Do App')]")
        self.assertIsNotNone(element_3)
        self.assertEqual(element_3.get_tag_name(), "h2")
        self.assertFalse(element_3.is_hidden())
        self.assertEqual(element_3.get_text(), "To Do App")

        # doesn't exist elements
        try:
            driver.find_element(by=By.ID, value="notexistelement")
            self.fail()
        except NoSuchElementException:
            pass
        except Exception as e:
            self.fail(e)

        try:
            driver.find_element(by=By.XPATH, value="//a[contains(text(), 'notexistelement')]")
            self.fail()
        except NoSuchElementException:
            pass
        except Exception as e:
            self.fail(e)

        driver.exit()
        sleep(self.SLEEP_TIME_AFTER_TEST)

    def test_find_elements(self):
        url_1 = "https://www.bbc.com/"
        driver = get_scraping_driver(via_request=self.USE_REQUEST_DRIVER, headless=self.HEADLESS)
        driver.get_url(url=url_1)
        elements_xpath_1 = "//li[contains(@class, 'media-list__item media-list__item--')]"
        elements_1 = driver.find_elements(by=By.XPATH, value=elements_xpath_1)
        self.assertTrue(len(elements_1) > 30)
        for element in elements_1:
            self.assertIsNotNone(element)

        if not self.HEADLESS and not self.USE_REQUEST_DRIVER:  # website blocking data in headless or requests
            url_2 = "https://www.iaa.gov.il/airports/ben-gurion/flight-board"
            driver.get_url(url=url_2)
            elements_xpath_2 = "//tr[contains(@class, 'flight_row')]"
            elements_2 = driver.find_elements(by=By.XPATH, value=elements_xpath_2)
            self.assertTrue(len(elements_2) > 0)
            for element in elements_2:
                self.assertIsNotNone(element)
                self.assertEqual(element.get_tag_name(), 'tr')
                self.assertNotEqual(element.get_text(), '')
                self.assertFalse(element.is_hidden())
                self.assertEqual(element.get_attribute("role"), 'row')

        # doesn't exist elements
        not_exist_elements_xpath = "//li[contains(@id, 'notexistelement')]"
        not_exist_elements_1 = driver.find_elements(by=By.XPATH, value=not_exist_elements_xpath)
        self.assertTrue(len(not_exist_elements_1) == 0)

        not_exist_elements_2 = driver.find_elements(by=By.ID, value="notexistelement")
        self.assertTrue(len(not_exist_elements_2) == 0)

        driver.exit()
        sleep(self.SLEEP_TIME_AFTER_TEST)


if __name__ == '__main__':
    import unittest

    unittest.main(module=__name__)
