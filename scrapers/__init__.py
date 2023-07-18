from server_utils.logger import get_current_logger
from scrapers.websites_scrapers.bbc_scraper import BBCScraper
from scrapers.websites_scrapers.nbc_scraper import NBCScraper
from scrapers.websites_scrapers.time_scraper import TIMEScraper
from scrapers.websites_scrapers.utils.exceptions import UnknownWebsiteScraperException
from scrapers.websites_scrapers.website_scraper_base import WebsiteScraperBase

SCRAPERS = {"bbc": BBCScraper, "time": TIMEScraper, "nbc": NBCScraper}


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
        return SCRAPERS[scraper_name](*args, **kwargs)
    except KeyError:
        desc = f"Cannot find scraper name: `{scraper_name}` in {SCRAPERS.keys()}"
        logger.error(desc)
        raise UnknownWebsiteScraperException(desc)
    except Exception as e:
        desc = f"Error getting website scraper instance of name: `{scraper_name}` - {str(e)}"
        logger.error(desc)
        raise e
