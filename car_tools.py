import sys, os, time, jellyfish
from scipy.stats import kendalltau, tmean, tstd
from own_parsers.car.cheaptickets import CheapticketsParser
from own_parsers.car.expedia import ExpediaParser
from own_parsers.car.orbitz import OrbitzParser
from own_parsers.car.priceline import PricelineParser
from own_parsers.car.priceline2 import PricelineParser as PricelineParser2
from own_parsers.car.travelocity import TravelocityParser

keywords = ['bangkok1', 'cairo1', 'cancun1', 'florence1', 'honolulu1',
            'lasvegas1', 'london1', 'miami1', 'montreal1', 'paris1',
            'bangkok2', 'cairo2', 'cancun2', 'florence2', 'honolulu2',
            'lasvegas2', 'london2', 'miami2', 'montreal2', 'paris2']
 
control = 'control'

parsers = {'cheaptickets': CheapticketsParser,
           'expedia': ExpediaParser,
           'orbitz': OrbitzParser,
           'priceline': PricelineParser,
           'travelocity': TravelocityParser,
}
 
def parse(car, fname):
    if car != 'priceline': lines = parsers[car](fname).parse()['data'].split('\n')  
    else:
        try:
            lines = parsers[car](fname).parse()['data'].split('\n')  
        except:
            lines = PricelineParser2(fname).parse()['data'].split('\n')  

    items = []  
    for line in lines:  
        if len(line) < 2: continue  
        e = line.split('\t')  
        items.append((e[0], e[1], float(e[2])))  
    return items

def avg_page_price(page):
    return tmean([price for comp, item, price in page])

def avg_page_price_diff(page1, page2):
    p1 = [price for comp, item, price in page1]  
    p2 = [price for comp, item, price in page2]  
    return tmean(p2) - tmean(p1)  

def different_prices(page1, page2):
    common = set([(comp, item) for comp, item, price in page1]) & set([(comp, item) for comp, item, price in page2])  
    p1 = {(comp, item):price for comp, item, price in page1}  
    p2 = {(comp, item):price for comp, item, price in page2}  
    diff = []  
    for pair in common:  
        d = p2[pair] - p1[pair]  
        if d != 0: diff.append(d)  
    return (len(common), diff) 

def safe_tstd(l):
    if len(l) <= 1: return 0
    return tstd(l)

