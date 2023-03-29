from scrapers.scraper_component.chrome_driver import ChromeDriver
from scrapers.scraper_component.requests_driver import RequestsDriver


def get_scraping_driver(via_request: bool = True, *args, **kwargs):
    if via_request:
        return RequestsDriver(*args, **kwargs)
    else:
        return ChromeDriver(*args, **kwargs)
