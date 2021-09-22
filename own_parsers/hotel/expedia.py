from hotel import HotelParser

class ExpediaParser(HotelParser):

	def __init__(self, html_file):
		super(ExpediaParser, self).__init__(html_file)
		self.hotel_name_selector = '.hotelWrapper .segment.hotel .details.showMile .infoCol .hotelName.fakeLink .hotelName strong'
		self.price_selector = '.hotelWrapper .segment.hotel .details.showMile .priceCol .price'
		self.city_selector = 'header[id="hotelResultTitle"] .section-header-main'
		self.date_in_selector = 'input[id="inpStartDate"]'
		self.date_out_selector = 'input[id="inpEndDate"]'
		self.hotel_adfilter_selector = '.hotelWrapper .segment.hotel.travelAd .details.showMile .infoCol .hotelName.fakeLink .hotelName strong'
		self.price_adfilter_selector = '.hotelWrapper .segment.hotel.travelAd .details.showMile .priceCol .price'

	def parse_date_in(self):
		date_in = self.root.cssselect(self.date_in_selector)
		return date_in[0].value

	def parse_date_out(self):
		date_out = self.root.cssselect(self.date_out_selector)
		return date_out[0].value

	def parse_date(self):
		try:
			date = self.parse_date_in() + '-' + self.parse_date_out()
			if date == '01/21/2014-01/22/2014':
				return 'A'
			elif date == '12/27/2013-01/04/2014':
				return 'B'
			elif date == '05/09/2014-05/17/2014':
				return 'C'
		except: pass
		return 'Z'

	def parse_city(self):
		try:
			my_city = self.root.cssselect(self.city_selector)[0].text_content()
			for city in self.city_list:
				if my_city.lower() in city.lower() or city.lower() in my_city.lower():
					return city 
		except: pass
		return None


	def parse_prices(self):
		acc = []
		prices = self.root.cssselect(self.price_selector)
		filtered = self.root.cssselect(self.price_adfilter_selector)
		prices = [price for price in prices if price not in filtered]
		for price in prices:
			if len(price) == 1:
				my_price = price[0].text_content().strip().replace('$', '').replace(',', '')
			else:
				my_price = price[1].text_content().strip().replace('$', '').replace(',', '')
			acc.append(my_price)
		return acc

	def parse_hotels(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_name_selector)
		filtered = self.root.cssselect(self.hotel_adfilter_selector)
		hotels = [hotel for hotel in hotels if hotel not in filtered]
		for hotel in hotels:
			acc.append(hotel.text_content().strip())
		return acc
