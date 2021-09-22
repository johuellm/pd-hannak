from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class MacysParser(EcommerceParser):
	def __init__(self, html_file):
		super(MacysParser, self).__init__(html_file)	
		self.product_section_selector = ".productThumbnail"	
		self.product_selector = ".innerWrapper .shortDescription a.productThumbnailLink"
		self.price_selector = ".innerWrapper .prices span"
		self.price_sale_selector = '.innerWrapper .prices .priceSale'

	def parse_list(self):
		results = []
		product_sections = self.root.cssselect(self.product_section_selector)
		
		for product_section in product_sections:
			html = lxml.html.fromstring(lxml.html.tostring(product_section))
			products = html.cssselect(self.product_selector)
			prices = html.cssselect(self.price_selector)
			price_sale = html.cssselect(self.price_sale_selector)
			#default_prices = html.cssselect(self.default_price_selector)
			product_name = ''
			if len(products) == 1:
				product_name = products[0].text_content().strip()
			price = 'No price'
			#if len(default_prices) == 1:
			#	price = self.clean_price(default_prices[0].text_content())
			if len(prices) >= 1:
				price = self.clean_price(prices[len(prices) - 1].text_content())
			if len(price_sale) == 1:
				price = self.clean_price(price_sale[0].text_content())

			# Christo's fix for item with price 'On Sale'
			if price == 'On': price = 'No price'
			if '-' in price: price = price.split('-')[0].strip()

			#if len(sale_prices) == 1:
			#	price = self.clean_price(sale_prices[0].text_content())
			results.append(product_name + '\t' + price)
		
		return results

	def clean_price(self, price):
		return price.replace('\n', '').replace('Everyday Value', '').replace('Now', '').replace('Sale', '').replace('Your Choice', '').strip()
