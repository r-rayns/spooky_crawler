from spooky_crawler.middleware.article_classifier import Weighting
from spooky_crawler.helpers.spooky_classifications import ArticleClass

# keywords must be lowercase!

# regex matches from the top of the list.
# if a single term is present in any other keywords with 2+ terms
# ensure the 2+ terms come before the single term. Otherwise the single term will
# be counted but not the 2+ terms.
_common_weights = {
    'paranormal': 1,
    'supernatural': 1,
    'natural': -1,
    'fans': -1,
    'soap': -1,
    'frightfest': -2,
    'solved': -2,
    'movie': -2,
    'movies': -2,
    'musical': -2,
    'tv': -2,
    'virtual': -2,
    'performance': -2,
    'things': -2,
    'halloween': -4,
    'hallowe\'en': -4,
    'hallowe’en': -4,
    'crimestoppers': -100,
    'hoax': -100,
    'list': -100,
    'abuse': -100,
    'zombie knife': -100,
    'zombie knives': -100,
}

ghost_weighting = Weighting({
    'rolls royce': -4,
    'silver ghost': -4,
    'ghost town': -4,
    'ghost towns': -4,
    'ghost street': -4,
    'ghost streets': -4,
    'ghost world': -4,
    'ghost fishing': -4,
    'ghost net': -4,
    'ghost nets': -4,
    'ghost station': -4,
    'ghosts in the machine': -4,
    'ghost shark': -4,
    'ghost sharks': -4,
    'ghost train': -4,
    'ghost trains': -4,
    'fish': -1,
    'white as a ghost': 0,
    'time slip': 2,
    'apparition': 2,
    'paranormal investigator': 2,
    'haunted': 1,
    'seance': 1,
    'manifestations': 1,
    'manifestation': 1,
    'ghosts': 1,
    'ghost': 1,
    'old haunt': 0,
    'haunt': 1,
    **_common_weights},
    ArticleClass.GHOST.value)

ufo_weighting = Weighting({
    'ufo': 2,
    'ufos': 2,
    'flying saucer': 1,
    'flying saucers': 1,
    'black triangle diversion': -1,
    'black triangle': 1,
    'alien': 1,
    'extraterrestrial': 1,
    'cloud': -1,
    'monument': -1,
    'illegal': -1,
    'pyrotechnic': -100,
    'memorial': -100,
    'tribute': -100,
    'perfume': -100,
    **_common_weights},
    ArticleClass.UFO.value)

abc_weighting = Weighting({
    'big cat': 2,
    'cryptid': 1,
    'cryptozoology': 1,
    'mystery creature': 1,
    'mystery beast': 1,
    'puma': 1,
    'panther': 1,
    'lion': 1,
    **_common_weights},
    ArticleClass.ABC.value)
