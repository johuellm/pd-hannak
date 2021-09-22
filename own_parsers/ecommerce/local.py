from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html


class LocalParser(EcommerceParser):
    def __init__(self, html_file):
        super(LocalParser, self).__init__(html_file)
        self.product_section_selector =".card-group"
        self.product_selector = ".card-title"
        self.price_selector = ".card-price"
        self.sku_selector = ".attributes strong[class=sku]"

    def parse_list(self):
        #print("Parsing of local (list) activated")
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        #print(f"product_sections: {product_sections}")
        for product_section in product_sections:
            #print('Parsing: ')
            html = lxml.html.fromstring(lxml.html.tostring(product_section))
            #print(f"html: {html}")
            products = html.cssselect(self.product_selector)
            prices = html.cssselect(self.price_selector)
            skus = html.cssselect(self.sku_selector)
            #print(products)
            #print(prices)
            product_name = ''
            """
            if len(products) == len(skus) == 1:
                # product_name = products[0].text_content().strip() + '-' + skus[0].text_content().strip()
                product_name = skus[0].text_content().strip()
            price = 'No price'
            if len(prices) == 1:
                price = prices[0].text_content().strip()

            if 'Sale' in price:
                price = price.split()[1]
            """
            product_name = products[0].text_content().strip()
            price = prices[0].text_content().strip().split(" ")[0]
            #print(f"product name: {product_name}")
            #print(f"price: {price}")
            results.append(product_name + '\t' + price)
        #print(f"results: {results}")
        return results