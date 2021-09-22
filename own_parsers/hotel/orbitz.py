from hotel import HotelParser
import json

class OrbitzParser(HotelParser):

	def __init__(self, html_file):
		super(OrbitzParser, self).__init__(html_file)
		self.hotel_name_selector = '.hotelResultCardHiDensity'
		self.safari_name_selector = 'h2.header'
		self.price_selector = '.hotelResultCardHiDensity'
		self.safari_price_selector = 'div.leadPrice span'
		self.city_selector = '.searchBarForm .hotelSearch .group.searchByKeyword span label input'
		self.date_in_selector = '.startDate label input'
		self.date_out_selector = 'input[name="hotel.chkout"]'

	def parse_date_in(self):
		try:
			date_in = self.root.cssselect(self.date_in_selector)
			return date_in[0].value
		except:
			return ""

	def parse_date_out(self):
		try:
			date_out = self.root.cssselect(self.date_out_selector)
			return date_out[0].value
		except:
			return ""

	def parse_date(self):
		date = self.parse_date_in() + '-' + self.parse_date_out()
		if date == '1/2/14-1/4/14':
			return 'A'
		elif date == '12/27/13-1/4/14':
			return 'B'
		elif date == '5/9/14-5/17/14':
			return 'C'
		return 'Z'

	def parse_city(self):
		try:
			my_city = self.root.cssselect(self.city_selector)[0].value
			for city in self.city_list:
				if my_city.lower() in city.lower() or city.lower() in my_city.lower():
					return city 
		except:
			pass
		return None

	def parse_hotels(self):
		acc = []
		hotels = self.root.cssselect(self.hotel_name_selector)
		if hotels:
			for hotel in hotels:
				data = json.loads(hotel.attrib['data-map-info'])
				acc.append(data['name'].replace('&amp;', '&'))
		else:
		       data = self.root.cssselect(self.safari_name_selector)
		       for d in data:
			       acc.append(d.text)
		return acc

	def parse_dollar_amount(self, price_div, price):
		#try:
		if price[0] == '$':
			return price[1:]
		else:
			# price is in euros. this part contains the price in dollars
			text = price_div.find_class('secondaryPrice')[0].text_content().strip()
			text = text.split('$')
			text = text[1].split('\n')[0].strip()
			return text
		#except Exception as e:
		#	print "exception"
			#print price_div.find_class('secondaryPrice')
			#print price_div.text_content().strip()
			#print price_div.fromstring.cssselect('hotelPriceInfo')

	def parse_prices(self):
		acc = []
		prices = self.root.cssselect(self.price_selector)
		if prices:
			for price_div in prices:
				try:
					data = json.loads(price_div.attrib['data-map-info'])
					price = data['label']
				#print price
					acc.append(self.parse_dollar_amount(price_div, price))
				except Exception:
					acc.append('No Results')
		else:
			data = self.root.cssselect(self.safari_price_selector)
			for d in data:
				acc.append(d.text[1:])
		return acc







