from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class NeweggParser(EcommerceParser):
    def __init__(self, html_file):
        super(NeweggParser, self).__init__(html_file)
        self.product_section_selector = ".itemCell"
        self.product_selector = ".itemText .wrapper span.itemDescription"
        self.price_selector = ".price-current"

    def parse_list(self):
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        for product_section in product_sections:
            #html = lxml.html.fromstring(lxml.html.tostring(product_section))
            products = product_section.cssselect(self.product_selector)
            prices = product_section.cssselect(self.price_selector)
            product_name = ''
            if len(products) >= 1:
                product_name = self.clean_string(products[0].text_content().strip())
            price = 'No price'
            if len(prices) >= 1:
                price = self.clean_price(prices[0].text_content())
            if len(price) <= 1: price = 'No price'

            if '-' in price: price = price.split('-')[0]

            results.append(product_name + '\t' + price)
        return results

    def clean_string(self, str):
        return str.replace('\n', '').replace('\t', '').encode('ascii', 'replace')

    def clean_price(self, price):
        price = price.replace('\n', '').replace('\t', '').replace(' ', '').replace('from', '').replace('USD', '').replace('AUD', '').strip().encode('ascii', 'replace').replace('?', '-')
        if price.endswith('-'):
            return price[:-1]
        else:
            return price
