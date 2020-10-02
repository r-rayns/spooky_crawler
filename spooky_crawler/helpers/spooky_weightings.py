from spooky_crawler.middleware.article_classifier import Weighting
from spooky_crawler.helpers.spooky_classifications import ArticleClass

_common_weights = {
    'paranormal': 1, 
    'film': -2, 
    'films': -2, 
    'movie': -2, 
    'movies': -2,
    'tv': -2,
    'virtual': -2,
    'fans': -0.5, 
    'soap': -1, 
    'performance': -1, 
    'things': -10,
    'halloween': -10,
    'Hallowe\'en': -10,
    'hoax': -100,
    'list': -100,
    'abuse': -100,
    }

ghost_weighting = Weighting({
    'ghost': 1, 
    'ghosts': 1, 
    'apparition': 1,
    'spirt': 0.5, 
    'haunt': 0.5, 
    'haunted': 0.5, 
    'ghost town': -4,
    'ghost towns': -4,
    'ghost world': -4,
    'ghost fishing': -4,
    'ghost net': -4,
    'ghost station': -4,
    **_common_weights}, 
    ArticleClass.GHOST.value)

ufo_weighting = Weighting({
    'ufo': 1, 
    'ufos': 1,
    'flying saucer': 1,
    'flying saucers': 1,
    'black triangle': 1,
    'alien': 0.5,
    'extraterrestrial': 0.5, 
    'illegal': -1, 
    'perfume': -100,
    **_common_weights}, 
    ArticleClass.UFO.value)

weird_weighting = Weighting({
    'zombie': 0.5,
    'odd': 0.2,
    'weird': 0.2,
    'mystery': 0.1,
    'creepy': 0.1,
    **_common_weights},
    ArticleClass.WEIRD.value)
