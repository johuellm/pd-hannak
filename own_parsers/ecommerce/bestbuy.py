from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class BestBuyParser(EcommerceParser):
	def __init__(self, html_file):
		super(BestBuyParser, self).__init__(html_file)	
		self.product_section_selector = ".hproduct"	
		self.product_selector = "h3[itemprop=name] a"
		self.price_selector = ".info-side .price.sale span"
		self.sku_selector = ".attributes strong[class=sku]"

	def parse_list(self):
		results = []
		product_sections = self.root.cssselect(self.product_section_selector)
		
		for product_section in product_sections:
			html = lxml.html.fromstring(lxml.html.tostring(product_section))
			products = html.cssselect(self.product_selector)
			prices = html.cssselect(self.price_selector)
			skus = html.cssselect(self.sku_selector)
			product_name = ''
			if len(products) == len(skus) == 1:
				#product_name = products[0].text_content().strip() + '-' + skus[0].text_content().strip()
				product_name = skus[0].text_content().strip()
			price = 'No price'
			if len(prices) == 1:
				price = prices[0].text_content().strip()
			
			if 'Sale' in price:
				price = price.split()[1]

			results.append(product_name + '\t' + price)
		
		return results
