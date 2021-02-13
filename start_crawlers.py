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
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_logger(name, log_path, log_name):
    Path(log_path).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    file_path = log_path + '/' + log_name
    # max logger size 500MB, mode a = appending
    file_handler = RotatingFileHandler(file_path, mode='a',
                                       maxBytes=500*1024*1024, backupCount=1, encoding=None, delay=0)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


# For testing purposes
# class Rrayn(SpookySpider):
    # name = "rrayn"
    # job_dir = 'crawls/rrayn'
    # custom_settings = {'JOBDIR': job_dir}
    # sitemap_urls = ['https://www.rrayns.co.uk/robots.txt']
    # logger = create_logger('spider.rrayn', job_dir, 'rrayn.log')


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


def sleep(self, *args, seconds, logger):
    """Non blocking sleep callback"""
    logger.info('Sleeping...')
    return deferLater(reactor, seconds, lambda: None)


def _crawl(result, spider, parser, logger, date_threshold=None):
    logger.info('🕷 Begin crawl for: {}, using date_threshold: {}'.format(
        spider.name, date_threshold))
    deferred = process.crawl(spider, parser, date_threshold, logger)
    # take current date, this will be used to check against last mod date on the next crawl
    crawl_start_date = datetime.utcnow()
    date_threshold = pytz.utc.localize(crawl_start_date)
    deferred.addCallback(sleep, seconds=86400, logger=logger)
    deferred.addCallback(_crawl, spider, parser, logger, date_threshold)
    return deferred


# _crawl(None, Rrayn, ArticleParser(
#     'Rrayn', Rrayn.logger).parse_article, Rrayn.logger)

_crawl(None, SpookyLiverpool, ArticleParser(
    'Liverpool Echo', SpookyLiverpool.logger).parse_article, SpookyLiverpool.logger)
_crawl(None, SpookyManchester, ArticleParser(
    'Manchester Evening News', SpookyManchester.logger).parse_article, SpookyManchester.logger)
_crawl(None, SpookyYorkshire, ArticleParser(
    'Yorkshire Evening Post', SpookyYorkshire.logger).parse_article, SpookyYorkshire.logger)
_crawl(None, SpookyPlymouth, ArticleParser(
    'Plymouth Herald', SpookyPlymouth.logger).parse_article, SpookyPlymouth.logger)
process.start()
