from logger import get_current_logger
from scrapers.web_scraper.websites_scrapers.bbc_scraper import BBCScraper
from scrapers.web_scraper.websites_scrapers.nbc_scraper import NBCScraper
from scrapers.web_scraper.websites_scrapers.time_scraper import TIMEScraper
from scrapers.web_scraper.websites_scrapers.utils.consts import ScraperConsts
from scrapers.web_scraper.websites_scrapers.utils.exceptions import UnknownWebsiteScraperException
from scrapers.web_scraper.websites_scrapers.website_scraper_base import WebsiteScraperBase


def websites_scrapers_factory(scraper_name: str, *args, **kwargs) -> WebsiteScraperBase:
    """
    Website scrapers factory of given `scraper_name` returning website scraper class instance
    :param scraper_name:
    :param args:
    :param kwargs:
    :return:
    """
    logger = get_current_logger()
    try:
        return ScraperConsts.DOMAINS_HOME_PAGE_URLS[scraper_name](*args, **kwargs)
    except KeyError:
        desc = f"Cannot find scraper name: `{scraper_name}` in {ScraperConsts.DOMAINS_HOME_PAGE_URLS.keys()}"
        logger.error(desc)
        raise UnknownWebsiteScraperException(desc)
    except Exception as e:
        desc = f"Error getting website scraper instance of name: `{scraper_name}` - {str(e)}"
        logger.error(desc)
        raise e
