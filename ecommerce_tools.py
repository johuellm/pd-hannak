import sys, os, time, jellyfish, math
from scipy.stats import kendalltau, tmean, tstd

from own_parsers.ecommerce.bestbuy import BestBuyParser
from own_parsers.ecommerce.cdw import CdwParser
from own_parsers.ecommerce.homedepot import HomeDepotParser
from own_parsers.ecommerce.jcpenney import JCPenneyParser
from own_parsers.ecommerce.macys import MacysParser
from own_parsers.ecommerce.newegg import NeweggParser
from own_parsers.ecommerce.officedepot import OfficeDepotParser
from own_parsers.ecommerce.sears import SearsParser
from own_parsers.ecommerce.staples import StaplesParser
from own_parsers.ecommerce.walmart import WalmartParser
from own_parsers.ecommerce.local import LocalParser

keywords = {
    'bestbuy': ["controller","dashboard+mount","stylus","car+battery","alarm+clock","computer+bag",
                "bookcase","remote","wireless","keyboard","lamp","ethernet","tower","phone+case",
                "hdmi+cabple","speakers","surround+sound","memory","cd"],
    'cdw': ["batteries","copy+machines","monitors+23","lcd+televisions","headphones","speakers",
            "phones","digital+cameras","laser+printer","memory+cards","flash+drives","batteries",
            "webcameras","printer+color","calculator","mouse","keyboard","laptop+cases","car+phone",
            "flashlights"],
    'homedepot': ["flower+gardening","gloves","duct+tape","rigid+insulation","wood","frames",
                  "paint+supplies","sinks","toilet+seats","lamps","chair","cushions","shag+rugs",
                  "ladders","led+bulbs","front+doors","bathroom+cabinets","drills","bathroom+accessories",
                  "woodworking+tools"],
    'jcpenney': ["cook+ware","pillows","bathroom+accessories","art+supplies","lamps","drills","vases",
                 "clocks","area+rugs","woman+pants","scarfs","purses","baby+shower+gifts","sunglasses",
                 "boots","man+shirts","stroller","diapers","toddler+beds","infant+car+seats","chairs"],
    'macys': ["ties","coats","boots","fur","suits","slippers","pajamas","hats","sundress","necklace",
              "jeans","belts","nailpolish","cufflinks","shorts","gloves","rings","dishes","glasses","tea"],
    'newegg': ["monitors+23","lcd+televisions","headphones","speakers","phones","waterproof+digital+cameras",
               "laser+printer","copy+machine","memory+cards","flash+drives","batteries","web+cameras",
               "printer+color","e-book","calculator","mouse","keyboard","laptop+cases","flashlights","car+phone"],
    'officedepot': ["business+card","cabinet","red+folders","camcorders","tools",
                    "coffee+maker","pads","desk+lamp","interactive+whiteboard",
                    "notebooks","Photo+Paper","Post-it","letter+opener","Duct+Tape",
                    "Stamps","Desk+Accessories","boxes","Glue","Name+Labels","hard+drive"],
    'sears': ["chairs","cook+ware","pillows","bathroom+accessories","art+supplies","lamps",
              "drills","vases","clocks","area+rugs","woman+pants","scarfs","sunglasses","boots",
              "man+shirts","stroller","diapers","toddler+beds","infant+car+seats","baby+shower+gifts"],
    'staples': ["business+card","cabinet","red+folders","camcorders","tools",
                "coffee+maker","hard+drive","pads","desk+lamp",
                "interactive+whiteboard","Photo+Paper","Post-it","Notebooks",
                "Letter+opener","DuctTape","Stamps","Desk+Accessories",
                "boxes","Glue","Name+Labels"],
    'walmart': ["cook+ware","chairs","pillows","Bathroom+Accessories","art+supplies",
                "lamps","drills","vases","clocks","area+rugs","woman+pants","scarfs",
                "sunglasses","boots","man+shirts","strollers","diapers","toddler+beds",
                "infant+car+seats","baby+shower+gifts"],
    'local': ['dynamic_bfp', 'dynamic_cookies', 'dynamic_newusers',
              'personalized_bfp', 'personalized_cookies', 'personalized_newusers'
              'static_bfp', 'static_cookies', 'static_newusers']
}
 
control = 'control'
 
parsers = {'bestbuy': BestBuyParser,
           'cdw': CdwParser,
           'homedepot': HomeDepotParser,
           'jcpenney': JCPenneyParser,
           'macys': MacysParser,
           'newegg': NeweggParser,
           'officedepot': OfficeDepotParser,
           'sears': SearsParser,
           'staples': StaplesParser,
           'walmart': WalmartParser,
           'local': LocalParser
}
 
def parse(store, fname):
    #print("Parsing Started")
    lines = parsers[store](fname).parse().split('\n')
    items = []
    #print(f"lines: {lines}")
    for line in lines:
        if len(line) < 2: continue
        e = line.split('\t')
        try:
            items.append((e[0], e[1]))
        except:
            print(fname)
            print(line)
            #sys.exit()
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

    # convert prices to dollars
    p_uniq = []
    for item, price in uniq:
        try:
            price = float(price.replace('$', '').replace(',', ''))
        except:
            price = 0.0
        p_uniq.append((price, item))


    # sort the unique items
    uniq = p_uniq
    uniq.sort()
    uniq.reverse()

    # score the golden set
    k = min(l)
    z = __dcg__([price for price, item in uniq], k)
    if z == 0: z = 1

    # score the pages             
    r = []
    for page in pages:
        pscores = []
        for item, price in page:
            try:
                price = float(price.replace('$', '').replace(',', ''))
            except:
                price = 0.0
            pscores.append(price)
        r.append(__dcg__(pscores, k)/z)

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

    # convert prices to dollars
    p_uniq = []
    for item, price in uniq:
        try:
            price = float(price.replace('$', '').replace(',', ''))
        except:
            price = 0.0
        p_uniq.append((price, item))

    # sort the unique items
    uniq = p_uniq
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
        pscores = []
        for item, price in page:
            try:
                price = float(price.replace('$', '').replace(',', ''))
            except:
                price = 0.0
            pscores.append(scores[(item, price)])

        r.append(__dcg__(pscores, k)/z)

    return r
"""

def get_prices(page):
    return [float(price.replace('$', '').replace(',', '')) for item, price in page if price != 'No price']

def avg_page_price(page):
    return tmean(get_prices(page))

def avg_page_price_diff(page1, page2):
    p1 = get_prices(page1)                                                                                                 
    p2 = get_prices(page2)                                                                                                 
    return tmean(p2) - tmean(p1)                                                                                                          

def different_prices(page1, page2, extended=False):
    common = set([item for item, price in page1]) & set([item for item, price in page2])
    p1 = {item:price for item, price in page1}
    p2 = {item:price for item, price in page2}
    diff = []
    disc = []
    for item in common:
        try:
            price1 = float(p1[item].replace('$', '').replace(',', ''))
        except:
            continue
        try:
            price2 = float(p2[item].replace('$', '').replace(',', ''))
        except:
            continue
        d = price2 - price1
        if d != 0:
            diff.append(d)
            disc.append(item)
    if not extended: return (len(common), diff)
    return (len(common), diff, disc)

def safe_tstd(l):
    if len(l) <= 1: return 0
    return tstd(l)

