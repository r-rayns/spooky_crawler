import re


class ArticleClassifier():
    logger = None

    def __init__(self, weightings, logger):
        self.weightings = weightings
        self.logger = logger

    def classify_article(self, article):
        if not article:
            return None

        article_class = None
        highest_score = 0
        scores = []

        for weighting in self.weightings:
            scores.append((weighting.classification, self._score_article(
                article, weighting.weights)))

        self.logger.info('Article scores {}'.format(scores))

        # set article type to the highest scoring article
        for (score_class, score) in scores:
            if score >= 2 and score > highest_score:
                article_class = score_class
                highest_score = score

        return article_class

    def _score_article(self, article, weights):
        score = 0
        regex_value = ''
        # create regex from the term associated with each weight
        for index, (term, weight) in enumerate(weights.items()):
            if index < len(weights) - 1:
                regex_value += r'\b{}\b|'.format(term)
            else:
                regex_value += r'\b{}\b'.format(term)

        matches = re.findall(regex_value, article, re.IGNORECASE)

        self.logger.info('matches made: ', matches)

        for match in matches:
            score += weights[match.lower()]

        return score


class Weighting():
    def __init__(self, weights, classification):
        self.weights = weights
        self.classification = classification
