import scrapy
import os
from datetime import datetime, timedelta
import pytz
from spooky_crawler.spiders.spooky_spider import SpookySpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spooky_crawler.middleware.article_parser import ArticleParser
from typing import cast
from twisted.internet import reactor
from twisted.internet.task import deferLater
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from twisted.internet.interfaces import IReactorTime

def create_logger(name, log_path, log_name):
    Path(log_path).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    file_path = log_path + '/' + log_name
    # max logger size 500MB, mode a = appending
    file_handler = RotatingFileHandler(file_path, mode='a',
                                       maxBytes=500*1024*1024, backupCount=1, encoding=None, delay=False)
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

class SpookyLincolnshire(SpookySpider):
    name = "spooky_lincolnshire"
    job_dir = 'crawls/lincolnshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.lincolnshirelive.co.uk/robots.txt']
    logger = create_logger('spider.lincolnshire', job_dir, 'lincolnshire.log')

class SpookyHampshire(SpookySpider):
    name = "spooky_hampshire"
    job_dir = 'crawls/hampshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.hampshirelive.news/robots.txt']
    logger = create_logger('spider.hampshire', job_dir, 'hampshire.log')

class SpookyNorfolk(SpookySpider):
    name = "spooky_norfolk"
    job_dir = 'crawls/norfolk'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.norfolklive.co.uk/robots.txt']
    logger = create_logger('spider.norfolk', job_dir, 'norfolk.log')

class SpookyInverness(SpookySpider):
    name = "spooky_inverness"
    job_dir = 'crawls/inverness'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.inverness-courier.co.uk/_sitemaps/sitemap.xml']
    sitemap_follow = ['/_sitemaps/']
    logger = create_logger('spider.inverness', job_dir, 'inverness.log')

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
        logger.info('⚠ Error starting crawl!')
    return deferred

_crawl(None, SpookyLiverpool, ArticleParser(
    'Liverpool Echo', SpookyLiverpool.logger).parse_article, SpookyLiverpool.logger)
_crawl(None, SpookyManchester, ArticleParser(
    'Manchester Evening News', SpookyManchester.logger).parse_article, SpookyManchester.logger)
_crawl(None, SpookyYorkshire, ArticleParser(
    'Yorkshire Evening Post', SpookyYorkshire.logger).parse_article, SpookyYorkshire.logger)
_crawl(None, SpookyPlymouth, ArticleParser(
    'Plymouth Herald', SpookyPlymouth.logger).parse_article, SpookyPlymouth.logger)
_crawl(None, SpookyLincolnshire, ArticleParser(
    'Lincolnshire Live', SpookyLincolnshire.logger).parse_article, SpookyLincolnshire.logger)
_crawl(None, SpookyHampshire, ArticleParser(
    'Hampshire Live', SpookyHampshire.logger).parse_article, SpookyHampshire.logger)
_crawl(None, SpookyNorfolk, ArticleParser(
    'Norfolk Live', SpookyNorfolk.logger).parse_article, SpookyNorfolk.logger)
_crawl(None, SpookyInverness, ArticleParser(
    'Inverness Courier', SpookyInverness.logger).parse_article, SpookyInverness.logger)
process.start()
