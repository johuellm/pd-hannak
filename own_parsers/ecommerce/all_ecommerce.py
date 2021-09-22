import lxml.etree
import lxml.html


class EcommerceParser(object):
	# representation of an ecommerce own_parsers

	def __init__(self, html_file):
		self.html_file = html_file
		#print(f"html length. {html_file}")
		self.site_list = ['local', 'bestbuy', 'cdw', 'jcpenney', 'macys', 'newegg', 'officedepot', 'sears', 'staples', 'walmart']
		f = open(html_file)
		self.root = lxml.html.fromstring(f.read())
		#print(self.root)
		f.close()


	def parse_list(self):
		return ''

	def parse(self):
		results = self.parse_list()
		acc = ''
		if results is not None:
			for result in results:
				acc += result + '\n'
			return acc.strip()
		else:
			return None


