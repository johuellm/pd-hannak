import lxml.etree
import lxml.html

class CarParser(object):
	# representation of a car own_parsers
	
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
		self.city_list = ['bangkok', 'london', 'paris', 'cairo', 'cancun', 'florence', 'honolulu', 'mccarran','las', 'miami', 'montreal', 'nv', 'vespucci', 'heathrow', 'qc', 'gaulle',  ]
		f = open(html_file)
		self.root = lxml.html.fromstring(f.read())
		f.close()

	def parse_date(self):
		return 'Z'

	def parse_city(self):
		return ''

	def parse_table(self):
		return ''

	def parse_list(self):
		return ''

	def parse(self):
		my_dict = {}
		my_dict['city'] = self.parse_city()
		my_dict['date'] = self.parse_date()
		my_dict['data'] = self.parse_table()
		my_dict['data'] += self.parse_list()
		return my_dict

	def __str__(self):
		return self.parse_table() + self.parse_list()









