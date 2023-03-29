import os


class MainConsts:
    DEFAULT_ELEMENT_TIMEOUT = int(os.getenv(key="DEFAULT_ELEMENT_TIMEOUT", default=5))
    IMPLICITLY_WAIT_TIME = int(os.getenv(key="IMPLICITLY_WAIT_TIME", default=0))
    ELEMENT_SLEEPING_TIME = float(os.getenv(key="ELEMENT_SLEEPING_TIME", default=0.25))
    INSERT_TEXT_SLEEPING_TIME = float(os.getenv(key="INSERT_TEXT_SLEEPING_TIME", default=0.20))
    REQUEST_TIMEOUT = int(os.getenv(key="REQUEST_TIMEOUT", default=15))
    GET_URL_TRIES = int(os.getenv(key="REQUEST_TRIES", default=3))


class BrowserConsts:
    # hard coded
    BINARY_FIREFOX_PATH = "/snap/bin/firefox"
    WINDOWS = "windows"
    LINUX = "linux"
    CHROME = "chrome"
    FIREFOX = "firefox"

    # dynamic
    LINUX_DRIVER_PATH = os.getenv(key="LINUX_DRIVER_PATH", default="/usr/bin")
    # TODO: change WINDOWS_DRIVER_PATH default value to temp folder
    WINDOWS_DRIVER_PATH = os.getenv(key="WINDOWS_DRIVER_PATH", default=r"")
    LINUX_BROWSER_PATH = os.getenv(key="BROWSER_PATH", default="/tmp")
    WINDOWS_BROWSER_PATH = os.getenv(key="BROWSER_PATH", default=r"C:\BrowserProfiles\SeleniumDefaultBrowserProfiles")
    DEFAULT_BROWSER = os.getenv(key="DEFAULT_BROWSER", default=CHROME)

    # tabs
    NEW_TAB_URLS = ["data:,", "chrome://new-tab-page/"]
    NEW_TAB_TITLE = "New Tab"


class ElementsConsts:
    REQ_ELEMENT = "req"
    WEB_ELEMENT = "web"
    XML_ELEMENT = "xml"
