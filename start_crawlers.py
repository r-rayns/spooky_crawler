from datetime import datetime
import pytz
from crawlers import SpookyHampshire, SpookyInverness, SpookyLincolnshire, SpookyLiverpool, SpookyManchester, SpookyNorfolk, SpookyPlymouth, SpookyYorkshire
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spooky_crawler.middleware.article_parser import ArticleParser
from typing import cast
from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.internet.interfaces import IReactorTime
from dotenv import load_dotenv

# load the .env file
load_dotenv()
process = CrawlerProcess(get_project_settings())

def sleep(self, *args, seconds, logger):
    """Non blocking sleep callback"""
    logger.info('Sleeping...')
    # Call the "callLater" method, which is part of the IReactorTime interface
    return deferLater(cast(IReactorTime,reactor), seconds, lambda: None)

def _crawl(result, spider, parser, logger, date_threshold=None):
    logger.info('🕷 Begin crawl for: {}, using date_threshold: {}'.format(
        spider.name, date_threshold))
    deferred = None
    try:
        deferred = process.crawl(spider, parser, date_threshold, logger)
        # take current date, this will be used to check against last mod date on the next crawl
        crawl_start_date = datetime.utcnow()
        date_threshold = pytz.utc.localize(crawl_start_date)

        deferred.addCallback(sleep, seconds=86400, logger=logger) # 86400s = 24 hours
        deferred.addCallback(_crawl, spider, parser, logger, date_threshold)
    except:
        logger.info('⚠ Error starting crawl!', exc_info=True)
    return deferred

crawlers = [
  SpookyLiverpool,
  SpookyManchester,
  SpookyYorkshire,
  SpookyPlymouth,
  SpookyLincolnshire,
  SpookyHampshire,
  SpookyNorfolk,
  SpookyInverness
]

for crawler in crawlers:
    parser = ArticleParser(crawler.site_name, crawler.logger).parse_article
    _crawl(None, crawler, parser, crawler.logger)


process.start()