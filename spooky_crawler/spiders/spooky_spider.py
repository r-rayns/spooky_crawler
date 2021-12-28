import shutil
import os
import scrapy
import dateparser
import spooky_crawler.helpers.dom_selectors as dom
import spooky_crawler.helpers.spooky_weightings as weightings
from datetime import datetime
from spooky_crawler.middleware.article_classifier import ArticleClassifier
from spooky_crawler.middleware.extractor import Extractor


class SpookySpider(scrapy.spiders.SitemapSpider):
    parser = None
    date_threshold = None
    job_dir = None
    logger = None

    sitemap_follow = ['/sitemaps/']
    sitemap_rules = [('/news/', 'parser')]

    def __init__(self, parser, date_threshold, logger, **kwargs):
        self.logger = logger
        self.job_dir = self.custom_settings.get('JOBDIR')
        self.logger.info('Initalised spider, job_dir: {}'.format(self.job_dir))

        if date_threshold:
            date_store_write = open(self.job_dir + '/date_store.txt', 'w')
            date_store_write.write(date_threshold.isoformat())
            date_store_write.close()
            self.date_threshold = date_threshold
        else:
            try:
                date_store_read = open(self.job_dir + '/date_store.txt', 'r')
                self.date_threshold = dateparser.parse(
                    date_store_read.readline())
                self.logger.info(
                    'Date threshold loaded: {}'.format(self.date_threshold))
                date_store_read.close()
            except:
                self.date_threshold = None

        self.parser = parser
        super().__init__(**kwargs)

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = None
            if entry.get('lastmod', None):
                date_time = dateparser.parse(entry['lastmod'])
            if not self.date_threshold or not date_time or (date_time >= self.date_threshold):
                yield entry

    @classmethod
    def from_crawler(cls, crawler, parser, date_threshold, logger, *args, **kwargs):
        spider = cls(parser=parser, date_threshold=date_threshold,
                     logger=logger, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def _set_crawler(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(
            self.spider_idle, signal=scrapy.signals.spider_idle)

    def spider_idle(self):
        self.logger.info('Prevent spider closure')
        try:
            os.remove(self.job_dir + '/requests.seen')
            shutil.rmtree(self.job_dir + '/requests.queue')
        except Exception as err:
            self.logger.warning(
                'Could not delete existing requests in job_dir, err: {}'.format(err))
