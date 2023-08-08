from time import sleep
from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

from db_driver import get_current_db_driver
from db_utils.file_utils import FileUtils
from logger import get_current_logger, log_function
from scrapers.google_scraper.utils.consts import IconsScraperConsts
from scrapers.google_scraper.utils.exceptions import GetIconsScraperException
from scrapers.google_scraper.utils.trends_utils import TrendUtils
from scrapers.google_scraper.utils.xpaths import IconsScraperXPaths
from scrapers.web_scraper.scraper_drivers import get_scraping_driver
from server_consts import ServerTimeConsts


class GetIconsScraper:
    SEC_TO_SLEEP = ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES * 6  # 6 hours
    SEC_TO_SLEEP_ON_ERROR = ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES * 1  # 1 hours

    def __init__(self):
        self.logger = get_current_logger()
        self._db = get_current_db_driver()
        self._trend_utils = TrendUtils()
        self.driver_initialize = False
        self._init_web_driver()

    @log_function
    def _init_web_driver(self):
        if not self.driver_initialize:
            self._driver = get_scraping_driver(via_request=False)
            self.driver_initialize = True

    @log_function
    def _quit(self):
        self._driver.exit()
        self.driver_initialize = False

    @log_function
    def _get_home_page(self):
        if not self._driver.get_current_url() or not (self._driver.get_current_url() in IconsScraperConsts.URL):
            self._driver.get_url(IconsScraperConsts.URL)

    @log_function
    def _search(self, term: str):
        search_exists = self._driver.is_element_appears(
            by=By.XPATH, value=IconsScraperXPaths.search, timeout=IconsScraperConsts.CRITICAL_ELEMENT_TIMEOUT
        )
        if search_exists:
            self._driver.insert_text(by=By.XPATH, value=IconsScraperXPaths.search, text=term)
            return
        desc = f"Failed to search term, cannot find search element -> `{IconsScraperXPaths.search}`"
        self.logger.error(desc)
        raise GetIconsScraperException(desc)

    @log_function
    def _clear_search(self):
        search_exists = self._driver.is_element_appears(
            by=By.XPATH, value=IconsScraperXPaths.search, timeout=IconsScraperConsts.CRITICAL_ELEMENT_TIMEOUT
        )
        if search_exists:
            self._driver.clear_input(by=By.XPATH, value=IconsScraperXPaths.search)
            return
        desc = f"Failed to clear search bar, cannot find search element -> `{IconsScraperXPaths.search}`"
        self.logger.error(desc)
        raise GetIconsScraperException(desc)

    @log_function
    def _get_icons_from_page(self) -> List[dict]:
        data: List[dict] = []
        media_icons_appears = self._driver.is_element_appears(
            by=By.XPATH, value=IconsScraperXPaths.media_icon, timeout=IconsScraperConsts.CRITICAL_ELEMENT_TIMEOUT
        )
        if not media_icons_appears:
            self.logger.error(f"Media icons didn't appears")
        media_icons = self._driver.find_elements(by=By.XPATH, value=IconsScraperXPaths.media_icon)
        for try_counter in range(IconsScraperConsts.TIMES_TO_TRY_GET_ICONS_FROM_PAGE):
            try:
                for media_icon in media_icons:
                    media_element = media_icon.real_element.find_element(
                        by=By.XPATH, value=IconsScraperXPaths.media_text
                    )
                    media = media_element.get_attribute("innerText")
                    src = media_icon.get_attribute("src")
                    data.append({"media": media, "src": src})
                    self.logger.debug(f"Got icon: `{media}` -> `{src}`")
                    return data
            except StaleElementReferenceException:
                media_icons = self._driver.find_elements(by=By.XPATH, value=IconsScraperXPaths.media_icon)
            except Exception as e:
                self.logger.error(f"Error getting icons NO. {try_counter + 1}/{len(media_icons)}, except: {str(e)}")

        return data

    @log_function
    def _save_data(self, data_list):
        if IconsScraperConsts.SAVE_TO_DB:
            for data in data_list:
                if self._db.exists(table_name="media", data_filter={"media": data["media"]}):
                    self.logger.warning(f"data is already exists for {data['media']}")
                    continue
                if IconsScraperConsts.SAVE_IMG:
                    file_path = FileUtils().save_image_from_url(url=data["src"], image_name=f"{data['media']}.png")
                    if file_path:
                        data.update({"file_path": file_path})
                        self._db.insert_one(table_name="media", data=data)
            self.logger.info(f"Inserted icons of trend to db -> `{data_list}`")

    @log_function
    def run(self):
        while True:
            try:
                self._init_web_driver()
                trends = self._trend_utils.get_popular_trends()
                get_icons_scraper._get_home_page()
                for trend in trends:
                    self._search(term=trend)
                    data_list = self._get_icons_from_page()
                    self._save_data(data_list)
                    self._clear_search()
                self.logger.info(f"Done collecting google articles")
                self._quit()
                sleep_time = self.SEC_TO_SLEEP
            except Exception as e:
                self.logger.error(f"Error run icons scraper, except: {str(e)}")
                sleep_time = self.SEC_TO_SLEEP_ON_ERROR
            desc = f"sleeping for {sleep_time / (ServerTimeConsts.SECONDS * ServerTimeConsts.MINUTES)} hours"
            self.logger.warning(desc)
            sleep(sleep_time)


if __name__ == '__main__':
    get_icons_scraper = GetIconsScraper()
    get_icons_scraper.run()
