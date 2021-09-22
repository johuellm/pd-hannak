import lxml.etree
import lxml.html
import sys
import datetime
import codecs
import inspect
import json
from random import randint
from expedia import ExpediaParser
from orbitz import OrbitzParser
from cheaptickets import CheapticketsParser
from travelocity import TravelocityParser
from priceline import PricelineParser

'''
Written by Gary Soeller

This script will parse a travel site for cars and their prices. 
This works by using the lxm library to search for html elements.
The main function is parseFile. Since each site is different, each site
has functions to properly grab the data from the html file. Before making 
any changes, I recommend looking at the site you are working on and comparing 
what you see the the classes in the store_obj class. 
'''

error_file = 'error_car.txt'
output_file = ''

#city_list = ['bangkok', 'london', 'paris', 'cairo', 'cancun', 'florence', 'honolulu', 'las vegas', 'miami', 'montreal', 'vespucci', 'heathrow', 'qc', 'gaulle',]
travel_sites = ['cheaptickets', 'expedia', 'hotels', 'kayak', 'orbitz', 'travelocity', 'priceline', 'venere']

'''Parsing and measurement'''
class store_obj(object):
	def __init__(self, store_name):
		# set store name
		self.store_name = store_name
		print '*********'+ store_name


# 		if store_name == 'priceline':
# 			self.agencies = {'HZ': 'Hertz', 'AV': 'Avis', 'BU': 'Budget', 'ET': 'Enterprise', 'AL': 'Alamo', 'NA': 'National'}
# 			self.car_agency_table_selector = '.partnerColumn .partnerRatesDiv .partnerCellWhite.cellFirst img'
# 			self.car_type_selector = '.carColumn .carGroupCellNew em'
# 			self.car_price_selector = '.partnerColumn .matrixPriceNew'
# 			self.car_date_in_selector = '.head-changesearch.group li'
# 			self.car_date_out_selector = '.head-changesearch.group li'
# 			self.car_city_selector = '.head-changesearch.group li'
# 			self.cool_cars_selector = '.coolcarsCell em'
# 			self.car_agency_list_selector = '.group .li-company img'
# 			self.car_price_list_selector = '.result .li-choose .price a'
# 			self.car_type_list_selector = '.result .car-title a'
		
# 		elif store_name == 'travelocity':
# 			self.agencies = {'FX': 'Fox','ET': 'Enterprise','ZR': 'Dollar','ZT': 'Thrifty','AL': 'Alamo','ZD': 'Budget','ZL': 'National','ZE': 'Hertz','ZA': 'Payless','AD': 'Advantage',
# 						'FF': 'Firefly','AC': 'Ace', 'EP': 'Europcar' "", 'SX' : 'Sixt', 'NA': 'Na', 'ZI': '_Zi', 'EZ': '_Ez', 'NU':'_Nu', 'EY':'_Ez'}
# #			self.agencies = {'et': 'Enterprise', 'al': 'Alamo', 'zl': 'National', 'ze': 'Hertz'}
# 			#self.car_agency_table_selector = 'table[id="resultsOne"] thead .carVendors .carVendor .thContain .vendor img'
# 			self.car_type_selector = 'table[id="availableCars"] tbody .carType .type a'
# 			self.car_price_selector = 'table[id="resultsOne"] tbody td'
# 			self.car_date_in_selector = '.wide.outerBar .wb_noad div[id="recap"] p'
# 			self.car_date_out_selector = '.wide.outerBar .wb_noad div[id="recap"] p'
# 			self.car_city_selector = '.wide.outerBar .wb_noad div[id="recap"] p'

		if store_name == 'hotels':
			self.car_agency_table_selector = '.carBlockHeaderBlueBar tbody tr td span b'
			self.car_type_selector = ''

		else:
			log('Invalid store name\t' + store_name)
			exit()



def log(message):
	# logs messages if running in production
	if sys.argv[4] == 'test':
		pass
	else:
		print message

# def get_pretty_date(store, date):
# 	if store.store_name in ['expedia', 'orbitz']:
# 		return 'Z'
# 	return 'Z'



# # parses the city from priceline
# def parse_priceline_city(my_city_list):
# 	my_city = my_city_list[0].text_content()
# 	for city in city_list:
# 		if city.lower() in my_city.lower() or my_city.lower() in city.lower():
# 			return city
# 	return None

# parses the city from the file
# def parseCity(file, store):
# 	try:
# 		f = open(file)
# 		root = lxml.html.fromstring(f.read())
# 		f.close()
# 		my_city_list = root.cssselect(store.car_city_selector)
# 
# 		if store.store_name == 'priceline':
# 			return parse_priceline_city(my_city_list)
# 	except Exception as e:
# 		log(e)


# def parseDate(file, store):
# 	try:
# 		f = open(file)
# 		root = lxml.html.fromstring(f.read())
# 		f.close()
# 		my_date_in_list = root.cssselect(store.car_date_in_selector)
# 		my_date_out_list = root.cssselect(store.car_date_out_selector)
# 
# # 		if store.store_name == 'travelocity':
# # 			pass
# 	except Exception as e:
# 		log(e)




# # get the table agencies from priceline
# def get_priceline_agencies(store, agency_list):
# 	acc = []
# 	for agency in agency_list:
# 		temp = agency.attrib['src'][-6:-4]
# 		if temp in store.agencies:
# 			if not store.agencies[temp] in acc:
# 				# we only want one occurrence of each agency once
# 				acc.append(store.agencies[temp])
# 		else:
# 			log('Agency does not exist:\t', temp)
# 			exit()
# 	return acc
# 
# # get the table prices from priceline
# def get_priceline_prices(price_list):
# 	acc = []
# 	for price in price_list:
# 		text = price.text_content().strip().replace('\n','').replace('\t','') + '\n'
# 		if text == 'N/A\n' or 'Inventory' in text:
# 			# no cars found
# 			acc.append('No Results')
# 		else:
# 			# has a price
# 			acc.append(text.split(' ')[0][1:])
# 	return acc

# # get the car types from the table for priceline
# def get_priceline_car_types(store, car_type_list, root):
# 	cool_cars_list = root.cssselect(store.cool_cars_selector)
# 	acc = []
# 	for car in car_type_list:
# 		acc.append(car.text_content())
# 	if len(cool_cars_list) > 0:
# 		# this cell doesnt have the same styles as the other cells
# 		acc.append('Fun Rides')
# 	return acc
# 
# # put all the priceline data for the table together
# def put_priceline_table_together(agency_list, price_list, car_type_list):
# 	num_cars = len(car_type_list)
# 	num_agencies = len(agency_list)
# 	i = 0
# 	acc = []
# 	while i < len(price_list):
# 		#print 'iterate'
# 		price = price_list[i]
# 		car = car_type_list[i%num_cars]
# 		agency = agency_list[int(i/num_cars)]
# 		#print price
# 		#print car 
# 		#print agency
# 		my_parsed = {'agency': agency,
# 					 'price': price,
# 					 'car': car}
# 		acc.append(my_parsed)
# 		#print acc
# 		i += 1
# 	return acc
# 
# # parse the agencies from the list in priceline
# def get_priceline_list_agencies(store, html_file):
# 	acc = []
# 	try:
# 		f = open(html_file)
# 		root = lxml.html.fromstring(f.read())
# 		f.close()
# 		agency_list = root.cssselect(store.car_agency_list_selector)
# 		for agency in agency_list:
# 			try:
# 				acc.append(store.agencies[agency.attrib['src'][-6:-4]])
# 			except Exception as e:
# 				log('Cannot find agency:\t' + agency.attrib['src'][-6:4])
# 				exit()
# 	except Exception as e:
# 		log(e)
# 	return acc
# 
# # parse the prices from the list in priceline
# def get_priceline_list_prices(store, html_file):
# 	acc = []
# 	try:
# 		f = open(html_file)
# 		root = lxml.html.fromstring(f.read())
# 		f.close()
# 		price_list = root.cssselect(store.car_price_list_selector)
# 		for price in price_list:	
# 			acc.append(price.text_content()[1:])
# 	except Exception as e:
# 		log(e)
# 	return acc
# 
# # parse the car types from the list in priceline
# def get_priceline_list_car_types(store, html_file):
# 	acc = []
# 	try:
# 		f = open(html_file)
# 		root = lxml.html.fromstring(f.read())
# 		f.close()
# 		car_types = root.cssselect(store.car_type_list_selector)
# 		for car in car_types:
# 			acc.append(car.text_content().strip()[:-1])
# 	except Exception as e:
# 		log(e)
# 	return acc
# 
# # puts everything togther for lists for priceline
# def put_priceline_list_together(list_agency_list, list_price_list, list_car_type_list):
# 	i = 0
# 	acc = []
# 	while i < len(list_agency_list):
# 		price = list_price_list[i]
# 		agency = list_agency_list[i]
# 		car_type = list_car_type_list[i]
# 		my_parsed = {'price': price,
# 					 'agency': agency,
# 					 'car': car_type}
# 		acc.append(my_parsed)
# 		i += 1
# 	return acc



def parseFile(html_file, error_file, store):
	#log("parsing... " + store.store_name)
	parsed = {}
	#date = get_pretty_date(store, parseDate(html_file, store))
	parsed['city'] = 'city' 
	parsed['date'] = 'Z'
	#print 'city\t', parsed['city'] 
	#print 'date\t' + parsed['date']
	
	try:
		'''
		f = open(html_file)
		root = lxml.html.fromstring(f.read())
		f.close()
		car_type_list = root.cssselect(store.car_type_selector)
		price_list = root.cssselect(store.car_price_selector)
		agency_list = root.cssselect(store.car_agency_table_selector)
		'''
		'''
		for car in car_type_list:
			print car.text_content()

		for price in price_list:
			print price
		'''

		if store == 'expedia':
			parser = ExpediaParser(html_file)
			return parser.parse()
			
		elif store == 'travelocity':
			parser = TravelocityParser(html_file)
			return parser.parse()
		
		elif store == 'orbitz':
			parser = OrbitzParser(html_file)
			return parser.parse()

		elif store == 'cheaptickets':
			parser = CheapticketsParser(html_file)
			return parser.parse()
		
		elif store == "priceline":
			parser = PricelineParser(html_file)
			return parser.parse()

# 		elif store == 'priceline':
# 			# the table part
# 			agency_list = get_priceline_agencies(store, agency_list)
# 			price_list = get_priceline_prices(price_list)
# 			car_type_list = get_priceline_car_types(store, car_type_list, root)
# 			parsed['data'] = put_priceline_table_together(agency_list, price_list, car_type_list)
# 			
# 			# the list part
# 			list_agency_list = get_priceline_list_agencies(store, html_file)
# 			list_price_list = get_priceline_list_prices(store, html_file)
# 			list_car_type_list = get_priceline_list_car_types(store, html_file)
# 			parsed['data'] += put_priceline_list_together(list_agency_list, list_price_list, list_car_type_list)
# 			return parsed

# 		elif store.store_name == 'travelocity':
# 			agency_list = get_travelocity_agencies(store, agency_list)
# 			price_list = get_travelocity_prices(price_list)
# 			car_type_list = get_travelocity_car_types(car_type_list)
# 			parsed['data'] = put_travelocity_list_together(agency_list, price_list, car_type_list)
# 			return parsed

		elif store == 'hotels':
			pass


	except Exception as e:
		#print 'error: '
		log(e)

def printParsed(parsed):
	try:
		f = codecs.open(output_file,encoding='utf-8', mode='a+')
		f.write(parsed['data'])
		#for item in parsed['data']:
		#	s = item['agency'] + '\t' + item['car'] + '\t' + item['price'] + '\n'
		#	f.write(s)
		f.close()
		log(output_file)
		log('success')
	except Exception as e:
		log(e)


log(sys.argv)
if len(sys.argv) < 5:
	log("Error: Too few arguments")
	exit()

store_name = sys.argv[1]


#store = store_obj(store_name)
store = store_name

html_file = sys.argv[2] 

parsed = parseFile(html_file, error_file, store)


city = parsed['city']
date = parsed['date']
if sys.argv[4] != 'test':
	output_file = sys.argv[3][:-4] + '_' + city + date + '.txt'
else:
	output_file = sys.argv[3]
printParsed(parsed)




