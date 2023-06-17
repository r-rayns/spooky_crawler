from spooky_crawler.spiders.spooky_spider import SpookySpider
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
                                       maxBytes=500*1024*1024, backupCount=1, encoding=None, delay=False)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

class SpookyLiverpool(SpookySpider):
    name = "spooky_liverpool"
    site_name = "Liverpool Echo"
    job_dir = 'crawls/liverpool'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.liverpoolecho.co.uk/robots.txt']
    logger = create_logger('spider.liverpool', job_dir, 'liverpool.log')


class SpookyManchester(SpookySpider):
    name = "spooky_manchester"
    site_name = "Manchester Evening News"
    job_dir = 'crawls/manchester'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.manchestereveningnews.co.uk/robots.txt']
    logger = create_logger('spider.manchester', job_dir, 'manchester.log')


class SpookyYorkshire(SpookySpider):
    name = "spooky_yorkshire"
    site_name = "Yorkshire Evening Post"
    job_dir = 'crawls/yorkshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.yorkshireeveningpost.co.uk/robots.txt']
    logger = create_logger('spider.yorkshire', job_dir, 'yorkshire.log')


class SpookyPlymouth(SpookySpider):
    name = "spooky_plymouth"
    site_name = "Plymouth Herald"
    job_dir = 'crawls/plymouth'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.plymouthherald.co.uk/robots.txt']
    logger = create_logger('spider.plymouth', job_dir, 'plymouth.log')

class SpookyLincolnshire(SpookySpider):
    name = "spooky_lincolnshire"
    site_name = "Lincolnshire Live"
    job_dir = 'crawls/lincolnshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.lincolnshirelive.co.uk/robots.txt']
    logger = create_logger('spider.lincolnshire', job_dir, 'lincolnshire.log')

class SpookyHampshire(SpookySpider):
    name = "spooky_hampshire"
    site_name = "Hampshire Live"
    job_dir = 'crawls/hampshire'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.hampshirelive.news/robots.txt']
    logger = create_logger('spider.hampshire', job_dir, 'hampshire.log')

class SpookyNorfolk(SpookySpider):
    name = "spooky_norfolk"
    site_name = "Norfolk Live"
    job_dir = 'crawls/norfolk'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.norfolklive.co.uk/robots.txt']
    logger = create_logger('spider.norfolk', job_dir, 'norfolk.log')

class SpookyInverness(SpookySpider):
    name = "spooky_inverness"
    site_name = "Inverness Courier"
    job_dir = 'crawls/inverness'
    custom_settings = {'JOBDIR': job_dir}
    sitemap_urls = ['https://www.inverness-courier.co.uk/_sitemaps/sitemap.xml']
    sitemap_follow = ['/_sitemaps/']
    logger = create_logger('spider.inverness', job_dir, 'inverness.log')