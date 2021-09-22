import lxml.etree
import lxml.html
import sys
import datetime
import codecs
import inspect
import json
from hotels import HotelsParser
from priceline import PricelineParser
from orbitz import OrbitzParser
from cheaptickets import CheapticketsParser
from expedia import ExpediaParser
from travelocity import TravelocityParser
from venere import VenereParser
import os



error_file = 'error_hotel.txt'
output_file = ''

city_list = ['bangkok', 'london', 'paris', 'cairo', 'cancun', 'florence', 'honolulu', 'las vegas', 'miami', 'montreal']
travel_sites = ['cheaptickets', 'expedia', 'hotels', 'kayak', 'orbitz', 'travelocity', 'priceline', 'venere']


def log(message):
	# logs messages if running in production
	if sys.argv[4] == 'test':
		pass
	else:
		print message

def printParsed(parsed):
	try:
		if os.path.isfile(output_file):
			printError({'error': 'File already exists\t' + output_file})
			exit()
		f = open(output_file, 'w')
		f.write(parsed['data'].encode('utf-8'))
		#for item in parsed['data']:
		#	s = item['agency'] + '\t' + item['car'] + '\t' + item['price'] + '\n'
		#	f.write(s)
		f.close()
		log('success')
	except Exception as e:
		log(e)

def printError(parsed):
	try:
		f = open(error_file, 'a')
		s = parsed['error'] + '\t' + html_file
		f.write(s.encode('utf-8') + '\n')
		f.close()
		log('error')
	except Exception as e:
		log(e)


def parseFile(html_file, error_file, store):
	#log("parsing... " + store.store_name)
	parsed = {}
	#city = parseCity(html_file, store)
	#date = get_pretty_date(store, parseDate(html_file, store))
	parsed['city'] = 'city' 
	parsed['date'] = 'Z'
	#print 'city\t', city 
	#print 'date\t' + date
	
	try:
		if store == 'hotels':
			parser = HotelsParser(html_file)
			return parser.parse()

		elif store == 'priceline':
			parser = PricelineParser(html_file)
			return parser.parse()

		elif store == 'orbitz':
			parser = OrbitzParser(html_file)
			return parser.parse()

		elif store == 'cheaptickets':
			parser = CheapticketsParser(html_file)
			return parser.parse()

		elif store == 'expedia':
			parser = ExpediaParser(html_file)
			return parser.parse()

		elif store == 'travelocity':
			parser = TravelocityParser(html_file)
			return parser.parse()

		elif store == 'venere':
			parser = VenereParser(html_file)
			return parser.parse()





	except Exception as e:
		log(e)




#log(sys.argv)
if len(sys.argv) < 5:
	log("Error: Too few arguments")
	exit()

store_name = sys.argv[1]
#log(store_name)

#store = store_obj(store_name)
store = store_name
for site in travel_sites:
	if site in store:
		store = site
		#log('Parsing ' + store + '...')
		break

html_file = sys.argv[2] 
parsed = parseFile(html_file, error_file, store)
city = parsed['city']
date = parsed['date']
if sys.argv[4] != 'test':
	output_file = sys.argv[3][:-4] + '_' + city + date + '.txt'
else:
	output_file = sys.argv[3]

if 'error' in parsed:
	printError(parsed)
else:
	printParsed(parsed)

