import dateparser
import spooky_crawler.helpers.dom_selectors as dom
import spooky_crawler.helpers.spooky_weightings as weightings
from datetime import datetime
from spooky_crawler.utils import Database
from spooky_crawler.middleware.article_classifier import ArticleClassifier
from spooky_crawler.middleware.extractor import Extractor


class ArticleParser():

    extractor = Extractor()

    classifier = None
    publisher_label = ''
    logger = None

    def __init__(self, publisher_label, logger):
        self.publisher_label = publisher_label
        self.logger = logger
        self.classifier = ArticleClassifier(
            [weightings.ghost_weighting, weightings.ufo_weighting,
                weightings.weird_weighting],
            logger)
        pass

    def parse_article(self, doc):
        print("\n" * 2)
        self.logger.info('Parse article with URL: {}'.format(doc.url))

        article_body = self.extractor.extract(
            doc, dom.article_body_selectors, 'articleBody')
        classification = self.classifier.classify_article(article_body)

        if not classification:
            self.logger.info('Article could not be classified')
            return

        self.logger.info('Article classified as {}'.format(classification))

        doc_date = self.extractor.extract(
            doc, dom.date_selectors, 'datePublished')
        pub_date = dateparser.parse(doc_date).isoformat()

        extractedData = {
            'publisher_id': None,
            'publisher': self.format_publisher_name(self.extractor.extract(doc, dom.publisher_selectors, 'publisher', 'name')),
            'date_published': pub_date,
            'date_retrieved': datetime.utcnow().isoformat(),
            'title': self.extractor.extract(doc, dom.title_selectors, 'headline'),
            'description': self.extractor.extract(doc, dom.description_selectors, 'description'),
            'link': doc.url,
            'article_type': classification
        }

        extractedData['publisher_id'] = self.get_publisher_id(extractedData)

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

    def get_publisher_id(self, extracted_data):
        if not extracted_data['publisher']:
            return None
        conn = Database(self.logger).connect()
        cursor = conn.cursor()
        # only select specific columns so we know the position they are returned in the array
        cursor.execute("""
             SELECT publisher_id, name FROM public.publishers
             WHERE name = '%s'
         """ % extracted_data['publisher'])

        publishers = cursor.fetchone()

        if not publishers:
            self.logger.info('Publisher not found, adding publisher...')
            try:
                cursor.execute("""
                 INSERT INTO publishers (name, label, lat_lng) VALUES ('%s', '%s', '0, 0')
                 RETURNING publisher_id
             """ % (extracted_data['publisher'], self.publisher_label))
                conn.commit()
                publishers = cursor.fetchone()
            except Exception as err:
                self.logger.warning(
                    'Could not add new publisher, error: {}'.format(err))

        cursor.close()
        return publishers[0]

    def store_article(self, article):
        conn = Database(self.logger).connect()
        cursor = conn.cursor()
        sql_insert = """
            INSERT INTO articles (
                publisher_id, 
                publisher, 
                date_published, 
                date_retrieved,
                title,
                description,
                link,
                article_type,
                accepted
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(sql_insert, (article['publisher_id'], article['publisher'], article['date_published'],
                                    article['date_retrieved'], article['title'], article['description'],
                                    article['link'], article['article_type'], False))
            conn.commit()
            cursor.close()
            self.logger.info('Stored article!')
        except Exception as err:
            self.logger.warning('Could not store article! Error: {}'.format(err))
