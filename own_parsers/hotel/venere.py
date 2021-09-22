from hotel import HotelParser

class VenereParser(HotelParser):

	def __init__(self, html_file):
		super(VenereParser, self).__init__(html_file)
		self.hotel_name_selector = '.hotelstrip .hotelstripinfo .hotel-name-and-stars h3'
		self.price_selector = '.hotelstrip .hotelstriprice'
		self.city_selector = 'input[id="city"]'
		self.date_in_selector = 'input[id="checkin"]'
		self.date_out_selector = 'input[id="checkout"]'

	def parse_date_in(self):
		date = self.root.cssselect(self.date_in_selector)[0]
		return date.value

	def parse_date_out(self):
		date = self.root.cssselect(self.date_out_selector)[0]
		return date.value

	def parse_date(self):
		date = self.parse_date_in() + '-' + self.parse_date_out()
		if date == '01/02/2014-01/04/2014':
			return 'A'
		elif date == '12/27/2013-01/04/2014':
			return 'B'
		elif date == '05/09/2014-05/17/2014':
			return 'C'
		return 'Z'

	def parse_city(self):
		my_city = self.root.cssselect(self.city_selector)[0].value
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
			price_div = price.find_class('hotelprice')
			price_div2 = price.find_class('pricediscount')
			if not price_div and not price_div2:
				new_price = 'No Results'
			elif not price_div2:
				new_price = price_div[0].text_content().strip()
			else:
				new_price = price_div2[0].text_content().strip()
			new_price = new_price.replace('$', '').strip()
			acc.append(new_price)

		return acc
