from car import CarParser
import lxml.etree
import lxml.html

# Parser for pages in list/grid view
class PricelineParser(CarParser):

	def __init__(self, html_file):
		super(PricelineParser, self).__init__(html_file)
		self.car_agency_table_selector ='.partnerRatesDiv .partnerCellWhite img'
		self.car_type_selector = '.carGroupCellNew em'
		self.car_price_selector = '.partnerColumn .priceCellNew .matrixPriceLink .matrixPriceNew'
		self.car_date_in_selector = '.contain-page .location'
		self.car_date_out_selector = '.contain-page .location'
		self.car_city_selector = '.contain-page .location'
		self.agencies = {'FX': 'Fox','ET': 'Enterprise','ZR': 'Dollar','ZT': 'Thrifty','AL': 'Alamo','ZD': 'Budget','ZL': 'National','ZE': 'Hertz','ZA': 'Payless','AD': 'Advantage',
						'FF': 'Firefly','AC': 'Ace', 'EP': 'Europcar' "", 'SX' : 'Sixt', 'NA': 'National', 'ZI': '_Zi', 'EZ': '_Ez', 'NU':'_Nu', 'EY':'_Ez','SV': 'Usave', 'BU' : 'budget', 'AV' : 'Avis', 'HZ' : 'Hertz' }


	def parse_date(self):
		my_date_list = self.root.cssselect(self.car_date_in_selector)
		my_list = my_date_list[0].text_content().split(' ')
		for el in my_list:
			if el.strip('.').lower() == "may":
				return "A"
			elif el.strip('.').lower() == "jun":
				return "B"
		return 'Z'

	
	def parse_city(self):
		my_city_list = self.root.cssselect(self.car_city_selector)
		my_text = my_city_list[0].text_content()
		my_list = my_text.split(' ')
		for el in my_list:
			for city in self.city_list:
				if city.lower() in el.lower() or el.lower() in city.lower():
					if city == "nv":
						city = 'las vegas'
					return city
					
		return None

	# gets the car types for expedia
	def get_priceline_car_types(self,car_type_list):
		acc = []
		for car in car_type_list:
			acc.append(car.text_content())
		return acc
	
	
	# gets the prices for expedia
	def get_priceline_prices(self, price_list):
		prices = []
		for price in price_list:
			elements = price.text_content().split('\n')
			for el in elements:
				if '$' in el or 'No Results' in el:
					prices.append(el.strip().replace('$', ''))
					break
		#print prices
		return prices 

		# gets the car types for priceline
	def priceline_car_types(self,car_type_list):
		acc = []
		for car in car_type_list:
			acc.append(car.text_content())
		return acc

		# gets the agencies for priceline
	def get_priceline_agencies(self, agency_list):
		acc = []
		for agency in agency_list:
			temp = agency.attrib['src'][-6:-4]
			if temp in self.agencies:
				acc.append(self.agencies[temp])
			else:
				print 'Cannot find agency...' + temp
		return acc 

	# put all of the prices and cars together to make it easy to print
	def put_priceline_together(self, price_list, car_type_list, agency_list):
		parsed = ''
		i = 0
		# this loop adds the cars from the table
		while i < len(price_list):
			price = price_list[i]
			if price == 'No Result':
				i+=1
				continue
			agency = agency_list[i%len(agency_list)]
			car = car_type_list[i/len(agency_list)]
		 	parsed += agency + '\t' + car + '\t' + price + '\n'
			i += 1
		return parsed 
	

	def parse_table(self):
		car_type_list = self.root.cssselect(self.car_type_selector)
		price_list = self.root.cssselect(self.car_price_selector)
		agency_list = self.root.cssselect(self.car_agency_table_selector)
		
		agency_list = self.get_priceline_agencies(agency_list)
		car_type_list = self.get_priceline_car_types(car_type_list)
		price_list = self.get_priceline_prices(price_list)
		return self.put_priceline_together(price_list, car_type_list, agency_list)



















