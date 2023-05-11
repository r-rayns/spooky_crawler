import os
import dateparser
import spooky_crawler.helpers.dom_selectors as dom
import spooky_crawler.helpers.spooky_weightings as weightings
import requests
from datetime import datetime
from spooky_crawler.middleware.article_classifier import ArticleClassifier
from spooky_crawler.middleware.extractor import Extractor
from logging import Logger
import traceback

class ArticleParser():

    extractor = Extractor()

    classifier: ArticleClassifier
    publisher_label = ''
    logger: Logger

    def __init__(self, publisher_label, logger):
        self.publisher_label = publisher_label
        self.logger = logger
        self.classifier = ArticleClassifier(
            [weightings.ghost_weighting, weightings.ufo_weighting,
                weightings.cryptid_weighting],
            logger)
        pass

    def parse_article(self, doc):
        print("\n" * 2)
        self.logger.info('Parse article with URL: {}'.format(doc.url))

        article_body = self.extractor.extract(
            doc, dom.article_body_selectors, 'articleBody')
        classification, matched_terms = self.classifier.classify_article(article_body)

        if not classification:
            self.logger.info('Article could not be classified')
            return

        self.logger.info('Article classified as {}'.format(classification))

        doc_date = self.extractor.extract(
            doc, dom.date_selectors, 'datePublished')

        parsed_date = dateparser.parse(doc_date)
        if not isinstance(parsed_date, datetime):
          self.logger.error('Parsed article publication date is not a valid datetime: }{}'.format(parsed_date))
          return

        pub_date = parsed_date.timestamp()

        extractedData = {
            'publisherName': self.format_publisher_name(self.extractor.extract(doc, dom.publisher_selectors, 'publisher', 'name')),
            'datePublished': int(pub_date),
            'dateRetrieved': int(datetime.utcnow().timestamp()),
            'title': self.extractor.extract(doc, dom.title_selectors, 'headline'),
            'description': self.extractor.extract(doc, dom.description_selectors, 'description'),
            'link': doc.url,
            'subject': classification,
            'matchedTerms': matched_terms
        }

        for value in extractedData:
            if not value:
                self.logger.warning('Not all data could be extracted, bail')
                return

        self.store_article(extractedData)
        return

    def format_publisher_name(self, publisher_name):
        if not publisher_name:
            return None
        return publisher_name.replace(" ", "").lower()

    def store_article(self, article):
        headers = {
            'Authorization': 'Bearer {}'.format(os.getenv('API_TOKEN'))}
        req = requests.post(
            '{}/api/articles'.format(os.getenv('HOST')), data=article, headers=headers)

        if(req.status_code == 200):
            self.logger.info('Stored article!')
        else:
            self.logger.warning(
                'Could not store article! \u001b[31mError: {}\u001b[0m'.format(req.json()))
            self.logger.info('Failed request: {}'.format(article))
