import sys, os, time, jellyfish, math
from scipy.stats import kendalltau, tmean, tstd

from own_parsers.hotel.cheaptickets import CheapticketsParser
from own_parsers.hotel.expedia import ExpediaParser
from own_parsers.hotel.hotels import HotelsParser
from own_parsers.hotel.orbitz import OrbitzParser
from own_parsers.hotel.priceline import PricelineParser
from own_parsers.hotel.travelocity import TravelocityParser
from own_parsers.hotel.venere import VenereParser

from own_parsers.hotel.cheapticketsAd import CheapticketsAdParser
from own_parsers.hotel.expediaAd import ExpediaAdParser
from own_parsers.hotel.hotelsAd import HotelsAdParser
from own_parsers.hotel.orbitzAd import OrbitzAdParser
from own_parsers.hotel.pricelineAd import PricelineAdParser
from own_parsers.hotel.travelocityAd import TravelocityAdParser
 
keywords = ['bangkok1', 'cairo1', 'cancun1', 'florence1', 'honolulu1',
            'lasvegas1', 'london1', 'miami1', 'montreal1', 'paris1',
            'bangkok2', 'cairo2', 'cancun2', 'florence2', 'honolulu2',
            'lasvegas2', 'london2', 'miami2', 'montreal2', 'paris2']
 
control = 'control'
 
parsers = {#'booking': BookingParser,                               
           'cheaptickets': CheapticketsParser,
           'expedia': ExpediaParser,
           'hotels': HotelsParser,
           #'kayak': KayakParser,
           'orbitz': OrbitzParser,
           'priceline': PricelineParser,
           'travelocity': TravelocityParser,
           'venere': VenereParser
}

ad_parsers = {
    'cheaptickets': CheapticketsAdParser,
    'expedia': ExpediaAdParser,
    'hotels': HotelsAdParser,
    'orbitz': OrbitzAdParser,
    'priceline': PricelineAdParser,
    'travelocity': TravelocityAdParser,
}
 
def parse(hotel, fname):
    return __parse__(parsers[hotel](fname).parse()['data'].split('\n'))

def parse_ads(hotel, fname):
    return __parse__(ad_parsers[hotel](fname).parse()['data'].split('\n'))

def __parse__(lines):
    items = []
    for line in lines:
        if len(line) < 2: continue
        e = line.split('\t')
        items.append((e[0], float(e[1])))
    return items    

def jaccard(page1, page2, extended=False):
    s1 = set(page1)
    s2 = set(page2)
    if len(s1) > len(s2):
        if not extended: return float(len(s1.intersection(s2)))/len(s1)
        return (float(len(s1.intersection(s2)))/len(s1), len(s1.intersection(s2)), len(s1))
    else:
        if not extended: return float(len(s2.intersection(s1)))/len(s2)
        return (float(len(s2.intersection(s1)))/len(s2), len(s2.intersection(s1)), len(s2))
 
def pages_to_alphabet(pages):
    s = set()
    for page in pages:
        for item in page:
            s.add(item)
    alph = {}
    for i, item in enumerate(s):
        alph[item] = chr(i + 96)
    return alph
 
def page_to_string(page, alph):
    s = ''
    for item in page:
        s += alph[item]
    return s

def editdist_and_kendalltau(page1, page2):
    alph = pages_to_alphabet([page1, page2])
    str1 = page_to_string(page1, alph)
    str2 = page_to_string(page2, alph)
    l1 = [a for a in str1]
    l2 = [a for a in str2]
    while len(l1) < len(l2): l1.append('null')
    while len(l2) < len(l1): l2.append('null')
    return (jellyfish.damerau_levenshtein_distance(str1, str2), kendalltau(l1, l2)[0])

def __dcg__(s, k):
    dcg = s[0]
    for i in range(1, k):
        dcg += s[i] / math.log(i + 1, 2)
    return dcg

def ndcg(pages):
    # locate all unique items
    uniq = set()
    l = []
    for page in pages:
        uniq = uniq.union(set(page))
        l.append(len(page))
    l.append(len(uniq))

    # sort the unique items
    uniq = [(price, item) for item, price in uniq]
    uniq.sort()
    uniq.reverse()
    
    # score the golden set
    k = min(l)
    z = __dcg__([price for price, item in uniq], k)
    if z == 0: z = 1

    # score the pages
    r = []
    for page in pages:
        r.append(__dcg__([price for item, price in page], k)/z)

    return r

"""
def __dcg__(s, k):
    dcg = 0.0
    for i in range(k):
        dcg += (math.pow(2, s[i])-1)/math.log(i+2,2)
    return dcg

def ndcg(pages):
    # locate all unique items
    uniq = set()
    l = []
    for page in pages:
        uniq = uniq.union(set(page))
        l.append(len(page))
    l.append(len(uniq))

    # sort the unique items
    uniq = [(price, item) for item, price in uniq]
    uniq.sort()
    uniq.reverse()
    
    # identify all unique ranks (throw out duplicate prices)
    u = set([price for price, item in uniq])
    gain = len(u) + 1

    # map each unique item to a ranked gain
    scores = {}
    prev = 99999999
    for price, item in uniq:
        if price != prev:
            prev = price
            gain -= 1
        scores[(item, price)] = gain

    # score the golden set
    k = min(l)
    z = __dcg__([scores[(item, price)] for price, item in uniq], k)
    if z == 0: z = 1

    # score the pages
    r = []
    for page in pages:
        r.append(__dcg__([scores[pair] for pair in page], k)/z)

    return r
"""

def avg_page_price(page):
    return tmean([price for item, price in page])

def avg_page_price_diff(page1, page2):
    p1 = [price for item, price in page1]                                                                                                 
    p2 = [price for item, price in page2]                                                                                                 
    return tmean(p2) - tmean(p1)                                                                                                          

def different_prices(page1, page2, extended=False):
    common = set([item for item, price in page1]) & set([item for item, price in page2])
    p1 = {item:price for item, price in page1}
    p2 = {item:price for item, price in page2}
    diff = []
    disc = []
    for item in common:
        d = p2[item] - p1[item]
        if d != 0:
            diff.append(d)
            disc.append(item)
    if not extended: return (len(common), diff)
    return (len(common), diff, disc)

def safe_tstd(l):
    if len(l) <= 1: return 0
    return tstd(l)

