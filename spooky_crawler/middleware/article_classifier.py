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
        article_terms = None
        highest_score = 0
        scores = []

        for weighting in self.weightings:
            self.logger.info('Getting score using {} weightings'.format(weighting.classification))
            article_score , matched_terms = self._score_article(
                article, weighting.weights)
            scores.append((weighting.classification, article_score, matched_terms))

        self.logger.info('Article scores {}'.format(scores))

        # set article type to the highest scoring article
        for (score_class, score, matched_terms) in scores:
            if score >= 2 and score > highest_score:
                article_class = score_class
                article_terms= matched_terms
                highest_score = score

        return article_class, article_terms

    def _score_article(self, article, weights):
        score = 0
        regex_value = ''
        # create regex from the term associated with each weight
        for index, (term, weight) in enumerate(weights.items()):
            if index < len(weights) - 1:
                regex_value += r'\b{}\b|'.format(term)
            else:
                regex_value += r'\b{}\b'.format(term)

        matched_terms = re.findall(regex_value, article, re.IGNORECASE)

        self.logger.info('Matches made: {}'.format(matched_terms))

        for match in matched_terms:
            score += weights[match.lower()]

        return score, matched_terms


class Weighting():
    def __init__(self, weights, classification):
        self.weights = weights
        self.classification = classification
