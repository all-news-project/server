import os
from platform import system

from logger import get_current_logger
from scrapers.scraper_component.utils.driver_consts import BrowserConsts
from scrapers.scraper_component.utils.exceptions import UnknownWebDriverException, UnknownOperatingSystemException, \
    UnknownBrowserException


def get_driver_path(browser_type: str) -> str:
    """
    Linux examples:
    >>> get_driver_path(browser_type=BrowserConsts.CHROME)
    '/usr/bin/chromedriver'

    >>> get_driver_path(browser_type=BrowserConsts.CHROME)
    r'C:/Drivers/chrome_drivers'

    :param browser_type:
    :return:
    """
    if browser_type == BrowserConsts.CHROME:
        webdriver_file_name = "chromedriver"
    else:
        raise UnknownWebDriverException(f"Unknown current web driver: '{browser_type}'")

    current_os = system().lower()
    path = ""
    if current_os == BrowserConsts.LINUX:
        path = BrowserConsts.LINUX_DRIVER_PATH
    elif current_os == BrowserConsts.WINDOWS:
        path = BrowserConsts.WINDOWS_DRIVER_PATH

    return os.path.join(path, webdriver_file_name)


def get_temp_browser_profile_path(browser_type: str) -> str:
    current_os = system().lower()
    if current_os == BrowserConsts.LINUX:
        path = os.path.join(BrowserConsts.LINUX_BROWSER_PATH, browser_type)
    elif current_os == BrowserConsts.WINDOWS:
        path = os.path.join(BrowserConsts.WINDOWS_BROWSER_PATH, browser_type)
    else:
        raise UnknownOperatingSystemException(f"Unknown operating system for run this driver: '{current_os}'")
    return os.path.join(path, "temp_browser_profile")


def create_path_if_needed(path: str):
    logger = get_current_logger()
    if os.path.isdir(path):
        logger.debug(f"Path '{path}' already exists")
    else:
        logger.warning(f"Path '{path}' not exits")
        try:
            logger.debug(f"Trying to creation directory path '{path}'")
            os.makedirs(path)
            logger.info(f"Path '{path}' created")
        except Exception as e:
            logger.error(f"Error creating directory path: '{path}' - {str(e)}")
            raise e


def kill_browser_childes(process_name: str):
    logger = get_current_logger()
    try:
        if process_name != BrowserConsts.CHROME and process_name != BrowserConsts.FIREFOX:
            raise UnknownBrowserException(f"No browser type: '{process_name}'")

        logger.debug(f"Trying to kill childes of process: '{process_name}'")
        file_name = f"{process_name}_pids.txt"
        os.system(f"pgrep -laf {process_name} > {file_name}")
        logger.debug(f"Saved pids to file: '{file_name}'")

        pids = []
        with open(file_name, "r") as f:
            for line in f.read().split("\n"):
                pid = line.split(" ")[0]
                if pid:
                    pids.append(pid)

        for pid in pids:
            logger.debug(f"Trying tp kill {process_name} process pid: '{pid}'")
            os.system(f"kill -9 {pid}")
            logger.info("Killed")

        logger.debug(f"Trying to remove file: '{file_name}'")
        os.remove(file_name)
        logger.info(f"Removed file: '{file_name}'")
    except Exception as e:
        logger.error(f"Error while trying to kill process of {process_name}")
        raise e


if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.FAIL_FAST)
    print("{} failures, {} driver_tests".format(failures, tests))
