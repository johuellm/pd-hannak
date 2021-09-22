from hotel import HotelParser

class HotelsParser(HotelParser):

	# '.hotel-name a'
	def __init__(self, html_file):
		super(self.__class__, self).__init__(html_file)
		self.hotel_name_selector = '.hotel:not(.sponsored) .hotel-description .hotel-name .hotelNameLink'
		#self.hotel_name_selector = '.hotel .hotel-description .hotel-name .hotelNameLink'
		self.price_selector = '.hotel .price-section .price-section-inner.clearfix'
		self.city_selector = '.c24.search-header-pinnable .search-form-wrapper .search-form.clearfix h1'
		self.date_in_selector = 'input[name="arrivalDate"]'
		self.date_out_selector = 'input[name="departureDate"]'

	def parse_date_in(self):
		return self.root.cssselect(self.date_in_selector)[0].value

	def parse_date_out(self):
		return self.root.cssselect(self.date_out_selector)[0].value

	def parse_date(self):
		try:
			date = self.parse_date_in() + '-' + self.parse_date_out()
			if date == '12/27/13-01/04/14':
				return 'B'
			elif date == '05/09/14-05/17/14':
				return 'C'
		except:
			pass
		return 'Z'

	def parse_city(self):
		city_list = self.root.cssselect(self.city_selector)
		try:
			my_city = city_list[0].text_content()
			for city in self.city_list:
				if my_city.lower() in city.lower() or city.lower() in my_city.lower():
					return city 
		except:
			pass
		return None

	def find_price(self, price_div):
		for price in price_div:
			# Christo Fix
			if price.attrib['class'] == 'urgency-message':
				return ''
			if price.attrib['class'] == 'price':
				for el in price:
					if el.tag == 'ins' or el.tag == 'span':
						return el.text_content().replace('$', '').replace(',', '')

	def parse_prices(self):
		acc = []
		prices = self.root.cssselect(self.price_selector)
		for price in prices:
			my_price = self.find_price(price)
			if my_price != '':
				# this gets rid of the sponsor prices
				acc.append(my_price)
		return acc

	def parse_hotels(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_name_selector)
		for hotel in hotels:
			acc.append(hotel.text_content().strip()) 
		return acc
