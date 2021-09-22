from car import CarParser
import lxml.etree
import lxml.html

class ExpediaParser(CarParser):
	
	def __init__(self, html_file):
		super(self.__class__, self).__init__(html_file)
		self.car_agency_table_selector = '.car-search-results.results-grid thead .grid-head .image-box img'
		self.car_type_selector = '.grid-row .car-class-target .car-class-label a'
		self.car_price_selector = 'tbody[id="grid-body"] .grid-row td'
		self.car_date_in_selector = '.playback-container .playback-text .text-container'
		self.car_date_out_selector = '.playback-container .playback-text .text-container'
		self.car_city_selector = '.playback-container .playback-text .text-container' 			
		self.agencies = {'FX': 'Fox','ET': 'Enterprise','ZR': 'Dollar','ZT': 'Thrifty','AL': 'Alamo','ZD': 'Budget','ZL': 'National','ZE': 'Hertz','ZA': 'Payless','AD': 'Advantage',
						'FF': 'Firefly','AC': 'Ace', 'EP': 'Europcar' "", 'SX' : 'Sixt', 'NA': 'National', 'ZI': '_Zi', 'EZ': '_Ez', 'NU':'_Nu', 'EY':'_Ez','SV': 'Usave'}
		



	def parse_date(self):
		my_date_list = self.root.cssselect(self.car_date_in_selector)
		my_list = my_date_list[1].text_content().split(' ')
		for el in my_list:
			if el.lower() == "may":
				return "A"
			elif el.lower() == "jun":
				return "B"
		return 'Z'
	
	
	def parse_city(self):
		my_city_list = self.root.cssselect(self.car_city_selector)
		my_city = my_city_list[0].text_content().split()[0]
		for city in self.city_list:
				if city.lower() in my_city.lower() or my_city.lower() in city.lower():
					#print city
					return city
		return None

	# gets the car types for expedia
	def get_expedia_car_types(self,car_type_list):
		acc = []
		for car in car_type_list:
			acc.append(car.text_content())
		return acc

	# gets the prices for expedia
	def get_expedia_prices(self, price_list):
		prices = []
		for price in price_list:
			elements = price.text_content().split('\n')
			for el in elements:
				#print el
				if '$' in el or 'No Results' in el:
					prices.append(el.strip().replace('$', ''))
					break
		return prices 

	# gets the agencies for expedia
	def get_expedia_agencies(self, agency_list):
		acc = []
		for agency in agency_list:
			temp = agency.attrib['src'][-6:-4]
			if temp in self.agencies:
				acc.append(self.agencies[temp])
			else:
				print 'Cannot find agency...' + temp
		return acc 


	# put all the prices and cars together to make it easy to print
	def put_expedia_together(self, price_list, car_type_list, agency_list):
		parsed = ''
		i = 0
		# this loop adds the cars from the table
		while i < len(price_list):
			price = price_list[i]
			if price == 'No Results':
				i += 1
				continue
			agency = agency_list[i%len(agency_list)]
			car = car_type_list[i/len(agency_list)]

			parsed += agency + '\t' + car + '\t' + price + '\n'
			i+=1
		return parsed

	def parse_table(self):
		car_type_list = self.root.cssselect(self.car_type_selector)
		price_list = self.root.cssselect(self.car_price_selector)
		agency_list = self.root.cssselect(self.car_agency_table_selector)
		
		agency_list = self.get_expedia_agencies(agency_list)
		car_type_list = self.get_expedia_car_types(car_type_list)
		price_list = self.get_expedia_prices(price_list)
		return self.put_expedia_together(price_list, car_type_list, agency_list)
