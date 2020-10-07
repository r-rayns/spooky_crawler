import scrapy
from datetime import datetime, timedelta
import pytz
from spooky_crawler.spiders.spooky_spider import SpookySpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spooky_crawler.middleware.article_parser import ArticleParser
from twisted.internet import reactor
from twisted.internet.task import deferLater
import logging
from pathlib import Path


def create_logger(name, log_path, log_name):
    Path(log_path).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    file_handler = logging.FileHandler(log_path + '/' + log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


class SpookyLiverpool(SpookySpider):
    name = "spooky_liverpool"
    job_dir = 'crawls/liverpool'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.liverpoolecho.co.uk/robots.txt']
    logger = create_logger('spider.liverpool', job_dir, 'liverpool.log')


class SpookyManchester(SpookySpider):
    name = "spooky_manchester"
    job_dir = 'crawls/manchester'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.manchestereveningnews.co.uk/robots.txt']
    logger = create_logger('spider.manchester', job_dir, 'manchester.log')


class SpookyYorkshire(SpookySpider):
    name = "spooky_yorkshire"
    job_dir = 'crawls/yorkshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.yorkshireeveningpost.co.uk/robots.txt']
    logger = create_logger('spider.yorkshire', job_dir, 'yorkshire.log')


class SpookyPlymouth(SpookySpider):
    name = "spooky_plymouth"
    job_dir = 'crawls/plymouth'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.plymouthherald.co.uk/robots.txt']
    logger = create_logger('spider.plymouth', job_dir, 'plymouth.log')


process = CrawlerProcess(get_project_settings())


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


def _crawl(spider, parser, logger, date_threshold=None):
    logger.info('🕷 Begin crawl for: {}, using date_threshold: {}'.format(
        spider.name, date_threshold))
    deferred = process.crawl(spider, parser, date_threshold, logger)
    # once finished take the date, this will be used to check against last mod date
    crawl_start_date = datetime.utcnow()
    date_threshold = pytz.utc.localize(crawl_start_date)
    deferred.addCallback(sleep, seconds=86400)
    deferred.addCallback(_crawl, spider, parser, logger, date_threshold,)
    return deferred


_crawl(SpookyLiverpool, ArticleParser(
    'Liverpool Echo', SpookyLiverpool.logger).parse_article, SpookyLiverpool.logger)
_crawl(SpookyManchester, ArticleParser(
    'Manchester Evening News', SpookyManchester.logger).parse_article, SpookyManchester.logger)
_crawl(SpookyYorkshire, ArticleParser(
    'Yorkshire Evening Post', SpookyYorkshire.logger).parse_article, SpookyYorkshire.logger)
_crawl(SpookyPlymouth, ArticleParser(
    'Plymouth Herald', SpookyPlymouth.logger).parse_article, SpookyPlymouth.logger)
process.start()
