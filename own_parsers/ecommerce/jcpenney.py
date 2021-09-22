from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class JCPenneyParser(EcommerceParser):
	def __init__(self, html_file):
		super(JCPenneyParser, self).__init__(html_file)	
		self.product_section_selector = ".product_holder"	
		self.product_selector = ".price_description .detail a"
		self.original_price_selector = ".pp_page_price.price_normal.flt_wdt"
		self.sale_price_selector = '.gallery_page_price.flt_wdt.comparisonPrice a'
		self.default_price_selector = '.gallery_page_price.flt_wdt a'

	def parse_list(self):
		results = []
		product_sections = self.root.cssselect(self.product_section_selector)
		
		for product_section in product_sections:
			html = lxml.html.fromstring(lxml.html.tostring(product_section))
			products = html.cssselect(self.product_selector)
			original_prices = html.cssselect(self.original_price_selector)
			sale_prices = html.cssselect(self.sale_price_selector)
			default_prices = html.cssselect(self.default_price_selector)
			product_name = ''
			if len(products) == 1:
				product_name = products[0].text_content().strip()
			price = 'No price'
			if len(default_prices) == 1:
				price = self.clean_price(default_prices[0].text_content())
			if len(original_prices) == 1:
				price = self.clean_price(original_prices[0].text_content())
			if len(sale_prices) == 1:
				price = self.clean_price(sale_prices[0].text_content())
			# Christo's fix for price ranges
			if '-' in price:
        		 price = price.split('-')[0].strip()

			results.append(product_name + '\t' + price)
		
		return results

	def clean_price(self, price):
		return price.replace('\n', '').replace('original', '').replace('sale', '').replace('clearance', '').strip()
