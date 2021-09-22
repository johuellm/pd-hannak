from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class SearsParser(EcommerceParser):
	def __init__(self, html_file):
		super(SearsParser, self).__init__(html_file)	
		self.product_section_selector = ".cardContainer.addToCartEnabled"	
		self.product_selector = ".cardInner .cardProdTitle h2[itemprop=name] a"
		self.featured_product_selector = ".cardInner .cardProdTitle h4 a"
		self.price_selector = ".cardInner .SubCatGalleryListView .cardProdPricing_v2.gridPrice span.price_v2.intShipHide"
		self.featured_price_selector = ".cardInner .cardProdPricing_v2 span.price_v2.intShipHide"
		self.product_part_number = ".cardInner input[id=prdPrtNo]"

	def parse_list(self):
		results = []
		product_sections = self.root.cssselect(self.product_section_selector)
		for product_section in product_sections:
			html = lxml.html.fromstring(lxml.html.tostring(product_section))
			products = html.cssselect(self.product_selector)
			featured_products = html.cssselect(self.featured_product_selector)
			prices = html.cssselect(self.price_selector)
			featured_prices = html.cssselect(self.featured_price_selector)
			product_number = html.cssselect(self.product_part_number)
			product_name = ''
			if len(products) == 1:
				product_name = products[0].text_content().strip()
			if len(featured_products) == 1:
				product_name = featured_products[0].text_content().strip()
			if len(product_number) == 1:
				product_name += '-' + product_number[0].value.strip()
			price = 'No price'
			if len(prices) >= 1:
				price = self.clean_price(prices[0].text_content())
			if len(featured_prices) == 1:
				price = self.clean_price(featured_prices[0].text_content())

			# Christo's fix for price ranges
			if '-' in price:
				price = price.split('-')[0].strip()

			results.append(product_name + '\t' + price)
		return results

	def clean_price(self, price):
		return price.replace('\n', '').replace('Everyday Value', '').replace('Now', '').replace('Sale', '').replace('Your Choice', '').strip()
