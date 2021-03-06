from car import CarParser
import lxml.etree
import lxml.html

class OrbitzParser(CarParser):

	def __init__(self, html_file):
		super(OrbitzParser, self).__init__(html_file)
		self.car_agency_table_selector = '.carResultsMatrixMod .control.matrix.carMatrix .company .link .headerLink'
		self.car_type_selector = '.carResultsMatrixMod .control.matrix.carMatrix .headerLink.rowHeader'
		self.car_type_attr = 'text'
		self.car_price_selector = '.carResultsMatrixMod .control.matrix.carMatrix tbody tr .unitPrice'
		self.car_price_attr = 'text'
		self.car_date_in_selector = '.carResultsSummaryMod .searchBarContent .summary .pipedList'
		self.car_date_in_attr = 'text'
		self.car_date_out_selector = '.carResultsSummaryMod .searchBarContent .summary .pipedList'
		self.car_date_out_attr = 'text'
		self.car_city_selector = '.carResultsSummaryMod .searchBarContent .summary .pipedList .newLine'
		self.car_city_attr = 'text'
		self.car_type_list_selector = '.carResultsCard .carItin .carItinerary .data dl'
		self.car_price_list_selector = '.carResultsCard .carPrice .priceDetails .changePrice'
		self.agency_selector = '.carResultsCard .carItinerary .brand'


	def parse_date(self):
		try:
			my_date_list = self.root.cssselect(self.car_date_in_selector)
			my_list = my_date_list[0].text_content().split(' ')
			for el in my_list:
				if el.lower() == "may":
					return "A"
				elif el.lower() == "jun":
					return "B"
		except:
			pass
		return 'Z'

	def parse_city(self):
		try:
			my_city_list = self.root.cssselect(self.car_city_selector)
			my_list = my_city_list[0].text_content().split('\n')
			for el in my_list:
				for city in self.city_list:
					if city.lower() in el.lower():
						return city
		except:
			pass
		return None

	
	# parses the prices from the table for orbitz
	def get_orbitz_prices(self, price_list):
		acc = []
		for price in price_list:
			for el in price:
				if el.tag == 'td':
					price = el.text_content().strip().replace("\n", '').replace('\t', '').split()
					if price == []:
						acc.append('No Results')
					else:
						acc.append(price[0].replace("$", '').replace(',', ''))
		return acc

	# parses the cars from the list of html elements
	def get_orbitz_cars(self, car_type_list):
		acc = []
		for car in car_type_list:
			acc.append(car.text_content())
		return acc

	# gets the agencies for orbitz
	def get_orbitz_agencies(self, agency_list):
		acc = []
		for agency in agency_list:
			acc.append(agency.text_content().strip())
		return acc

	# put all of the prices and cars together to make it easy to print
	def put_orbitz_table_together(self, price_list, car_type_list, agency_list):
		parsed = ''
		i = 0
		# this loop adds the cars from the table
		while i < len(price_list):
			price = price_list[i]
			agency = agency_list[i%len(agency_list)]
			car = car_type_list[i/len(agency_list)]
		 	parsed += agency + '\t' + car + '\t' + price + '\n'
			i += 1
		return parsed 
	
	# gets the car types from orbitz in the list part
	def get_orbitz_list_car_types(self):
		acc = []
		car_list = self.root.cssselect(self.car_type_list_selector)
		valid = True
		for car in car_list:
			i = 0
			car_type = ''
			if valid:
				for el in car:
					if i == len(car) - 1:
						break
					else:
						l = el.text_content().split()
						for s in l:
							car_type += s + ' '
							car_type.replace('\t', '')
						i+=1
				acc.append(car_type.strip())
				valid = False
			else:
				valid = True
		return acc


	# gets the agencies from orbitz in the list part
	def get_orbitz_list_agencies(self):
		acc = []
		agency_list = self.root.cssselect(self.agency_selector)
		for agency in agency_list:
			acc.append(agency.attrib['alt'].strip())
		return acc

	# gets the prices from orbitz in the list part
	def get_orbitz_list_prices(self):
		acc = []
		price_list = self.root.cssselect(self.car_price_list_selector)
		for price in price_list:
			acc.append(price.text_content().strip().replace('$', '').replace(',', ''))
		return acc

	# puts all of the list cars together for orbitz to make it easy to print
	def put_orbitz_list_together(self, price_list, car_type_list, agency_list):
		parsed = ''
		i = 0
		while i < len(price_list):
			price = price_list[i]
			agency = agency_list[i]
			car = car_type_list[i]
			parsed += agency + '\t' + car + '\t' + price + '\n'
			i += 1
		return parsed



	def parse_table(self):
		car_type_list = self.root.cssselect(self.car_type_selector)
		price_list = self.root.cssselect(self.car_price_selector)
		agency_list = self.root.cssselect(self.car_agency_table_selector)
		agency_list = self.get_orbitz_agencies(agency_list)
		price_list = self.get_orbitz_prices(price_list)
		car_type_list = self.get_orbitz_cars(car_type_list)


		list_price_list = self.get_orbitz_list_prices()
		list_agency_list = self.get_orbitz_list_agencies()
		list_car_type_list = self.get_orbitz_list_car_types()

		table_part = self.put_orbitz_table_together(price_list, car_type_list, agency_list)
		list_part = self.put_orbitz_list_together(list_price_list, list_car_type_list, list_agency_list)
		return table_part + list_part




















