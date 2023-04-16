from scrapers.scraper_drivers import get_scraping_driver

if __name__ == '__main__':
    driver = get_scraping_driver(via_request=False)
    print(driver.get_current_url())
