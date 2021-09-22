import lxml.etree
import lxml.html

class HotelParser(object):
	# representation of a hotel own_parsers
	
	''' WISHLIST
	need to parse the date
	need to parse the city
	need to parse table
		need to parse agencies
		need to parse car types
		need to parse prices
	need to parse list
		need to parse agencies
		need to parse car types
		need to parse prices
	'''
	def __init__(self, html_file):
		self.html_file = html_file
		self.city_list = ['bangkok', 'london', 'paris', 'cairo', 'cancun', 'florence', 'honolulu', 'las vegas', 'miami', 'montreal']
		f = open(html_file)
		self.root = lxml.html.fromstring(f.read())
		f.close()
		self.results = {}

	def parse_date(self):
		return 'Z'

	def parse_city(self):
		return ''

	def parse_hotels(self):
		return []

	def parse_prices(self):
		return []

	def put_together(self):
		prices = self.parse_prices()
		hotels = self.parse_hotels()
		#print prices
		if len(prices) != len(hotels):
			self.results['error'] = 'Found different number of prices and items'
			return ''
		else:
			i = 0
			acc = ''
			while i < len(prices):
				acc += hotels[i] + '\t' + prices[i] + '\n'
				i += 1
		return acc

	def parse(self):
		self.results['city'] = self.parse_city()
		self.results['date'] = self.parse_date()
		self.results['data'] = self.put_together()

		return self.results

	def __str__(self):
		return self.put_together()
