from car import CarParser
import lxml.etree
import lxml.html

# Parser for pages in list/grid view
class PricelineParser(CarParser):

	def __init__(self, html_file):
		super(PricelineParser, self).__init__(html_file)
		self.car_agency_selector = '.group .li-company img'
		self.car_type_selector = '.result .car-title a strong'
		self.car_price_selector = '.result .li-choose .price a'
		self.car_date_in_selector = '.head-changesearch.group li'
		self.car_date_out_selector = '.head-changesearch.group li'
		self.car_city_selector = '.head-changesearch.group li'
		self.agencies = {'FX': 'Fox','ET': 'Enterprise','ZR': 'Dollar','ZT': 'Thrifty','AL': 'Alamo','ZD': 'Budget','ZL': 'National','ZE': 'Hertz','ZA': 'Payless','AD': 'Advantage',
						'FF': 'Firefly','AC': 'Ace', 'EP': 'Europcar' "", 'SX' : 'Sixt', 'NA': 'National', 'ZI': '_Zi', 'EZ': '_Ez', 'NU':'_Nu', 'EY':'_Ez','SV': 'Usave', 'BU' : 'budget', 'AV' : 'Avis', 'HZ' : 'Hertz' }


	def parse_date(self):
		my_date_list = self.root.cssselect(self.car_date_in_selector)
		my_list = my_date_list[0].text_content().split(' ')
		for el in my_list:
			if el.lower() == "may." or el.lower() == "may":
				#print "A"
				return "A"
			elif el.lower() == "jun." or el.lower() == "jun":
				#print 'B'
				return "B"
		return 'Z'

	def parse_city(self):
		my_city_list = self.root.cssselect(self.car_city_selector)
		#print my_city_list
		my_list = my_city_list[0].text_content().split(' ')
		#print my_list
		for el in my_list:
			for city in self.city_list:
				if city.lower() in el.lower():
					#print '*********' + city
					return city
		return None


	# get the table agencies from priceline
	def get_priceline_agencies(store, agency_list):
		acc = []
		for agency in agency_list:
			if agency.attrib['src'][0:4] == "http": 
				temp = agency.attrib['src'][-6:-4]
				if temp in store.agencies:
					if not store.agencies[temp] in acc:
						# we only want one occurrence of each agency once
						acc.append(store.agencies[temp])
				else:
					print 'Agency does not exist:\t', temp
		return acc

	
	# gets the car types for priceline
	def get_priceline_car_types(self,car_type_list):
		acc = []
		for car in car_type_list:
			acc.append(car.text_content())
		return acc
	

	# gets the prices for priceline
	def get_priceline_prices(self, price_list):
		acc = []
		for price in price_list:
			#print price_list
			text = price.text_content().replace('\n','').replace('\t','') + '\n'
			if text == 'N/A\n' or 'Inventory' in text:
				# no cars found
				acc.append('No Results')
			else:
				# has a price
				acc.append(text.split(' ')[0][0:])
		return acc
		

	# put all of the prices and cars together to make it easy to print
	def put_priceline_together(self, price_list, car_type_list, agency_list):
		parsed = ''
		i = 0
		# this loop adds the cars from the table
		while i < len(price_list):
			price = price_list[i].replace('$', '')
			agency = agency_list[i%len(agency_list)]
			car = car_type_list[i/len(agency_list)]
		 	parsed += agency + '\t' + car + '\t' + price + '\n'
			i += 1
		return parsed 
	
	

	def parse_table(self):
		car_type_list = self.root.cssselect(self.car_type_selector)
		price_list = self.root.cssselect(self.car_price_selector)
		agency_list = self.root.cssselect(self.car_agency_selector)
		
		agency_list = self.get_priceline_agencies(agency_list)
		car_type_list = self.get_priceline_car_types(car_type_list)
		price_list = self.get_priceline_prices(price_list)
		return self.put_priceline_together(price_list, car_type_list, agency_list)
