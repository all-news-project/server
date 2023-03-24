from functools import cache

from scrapers.scraper_component.requests_driver import RequestsDriver


@cache
def get_scraping_driver(via_request: bool = True):
    if via_request:
        return RequestsDriver()
    # else:
    #     return WebDriver()
