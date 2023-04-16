from scrapers.scraper_drivers.chrome_driver import ChromeDriver
from scrapers.scraper_drivers.requests_driver import RequestsDriver


def get_scraping_driver(via_request: bool = True, *args, **kwargs):
    if via_request:
        return RequestsDriver(*args, **kwargs)
    else:
        return ChromeDriver(*args, **kwargs)
