from hotel import HotelParser

class HotelsAdParser(HotelParser):

	def __init__(self, html_file):
		super(self.__class__, self).__init__(html_file)
		self.hotel_selector = '.hotel .hotel-basic-info.clearfix'
		self.ad_selector = '.urgency-message'
		self.name_selector = '.hotel-name a'
		self.price_selector = '.price ins, .price span'
		self.city_selector = '.c24.search-header-pinnable .search-form-wrapper .search-form.clearfix h1'
		self.date_in_selector = 'input[name="arrivalDate"]'
		self.date_out_selector = 'input[name="departureDate"]'

	def parse_date_in(self):
		return self.root.cssselect(self.date_in_selector)[0].value

	def parse_date_out(self):
		return self.root.cssselect(self.date_out_selector)[0].value

	def parse_date(self):
		date = self.parse_date_in() + '-' + self.parse_date_out()
		if date == '01/21/2014-01/22/2014':
			return 'A'
		elif date == '12/24/2013-01/04/2014' or date == '12/24/13-1/4/14' or date == '12/24/2013-1/4/2014' or date == '12/27/13-01/04/14' or date == '12/27/2013-01/04/2014' or date == '12/27/13-1/4/14':
			return 'B'
		elif date == '05/09/2014-05/17/2014' or date == '5/9/14-5/17/14' or date == '5/9/2014-5/17/2014' or date == '05/09/14-05/17/14':
			return 'C'
		#print '**************' + date
		return 'Z'
	
	def parse_city(self):
		city_list = self.root.cssselect(self.city_selector)
		my_city = city_list[0].text_content()
		for city in self.city_list:
			if my_city.lower() in city.lower() or city.lower() in my_city.lower():
				return city 
		return None

	def parse_prices(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_selector)
		for hotel in hotels:
			urgent = hotel.cssselect(self.ad_selector)
			if len(urgent) > 0 and urgent[-1].text_content().strip().lower() == 'sponsored listing':
				acc.append(hotel.cssselect(self.price_selector)[0].text_content().strip()[1:]) 
		return acc

	def parse_hotels(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_selector)
		for hotel in hotels:
			urgent = hotel.cssselect(self.ad_selector)
			if len(urgent) > 0 and urgent[-1].text_content().strip().lower() == 'sponsored listing':
				acc.append(hotel.cssselect(self.name_selector)[0].text_content().strip()) 
		return acc
