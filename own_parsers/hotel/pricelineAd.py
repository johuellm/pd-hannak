# 6 ads on a page, 1 top, 2 bottom, 3 all over

from hotel import HotelParser

class PricelineAdParser(HotelParser):

	def __init__(self, html_file):
		super(self.__class__, self).__init__(html_file)
		self.hotel_name_selector = '.listitem_sponsored .listitem_name_link'
		self.price_selector = '.listitem_sponsored .listitem_price_amount'
		self.city_selector = 'input[id="cityName"]'
		self.date_in_selector = 'input[id="checkInDate"]'
		self.date_out_selector = 'input[id="checkOutDate"]'

	def parse_date_in(self):
		return self.root.cssselect(self.date_in_selector)[0].value

	def parse_date_out(self):
		return self.root.cssselect(self.date_out_selector)[0].value

	def parse_date(self):
		date = self.parse_date_in() + '-' + self.parse_date_out()
		if date == '01/21/2014-01/22/2014':
			return 'A'
		elif date == '12/24/2013-01/04/2014' or date == '12/24/13-1/4/14' or date == '12/24/2013-1/4/2014':
			return 'B'
		elif date == '05/09/2014-05/17/2014' or date == '5/9/14-5/17/14' or date == '5/9/2014-5/17/2014':
			return 'C'
		return 'Z'

	def parse_city(self):
		my_city = self.root.cssselect(self.city_selector)[0]
		my_city = my_city.attrib['value']
		for city in self.city_list:
			if my_city.lower() in city.lower() or city.lower() in my_city.lower():
				return city 
		return None

	def parse_hotels(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_name_selector)
		for hotel in hotels:
			acc.append(hotel.text_content().strip())
		return acc

	def parse_prices(self):
		acc = []
		prices = self.root.cssselect(self.price_selector)
		for price in prices:
			acc.append(price.text_content().replace('$', ''))
		return acc
