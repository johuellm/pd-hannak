from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class StaplesParser(EcommerceParser):
    def __init__(self, html_file):
        super(StaplesParser, self).__init__(html_file)    
        self.product_section_selector = ".prd"
        self.product_selector = ".prd .model"
        self.price_selector = ".prd .pricenew .pis i"
        
        
    def parse_list(self):
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        
        #skus = self.root.cssselect(self.sku_selector)
        if len(product_sections) != 0:
            products = self.root.cssselect(self.product_selector)
            prices = self.root.cssselect(self.price_selector)
            for product_section in product_sections:
                html = lxml.html.fromstring(lxml.html.tostring(product_section))                
                products = html.cssselect(self.product_selector)
                prices = html.cssselect(self.price_selector)
                product_name = ''
                #print products 
                if len(products) == 1:
                    product_name = products[0].text_content().strip()
                price = 'No price'
                if len(prices) == 1:
                    price = prices[0].text_content().strip()
                    if len(price.split()) > 1 : 
                        price = price.split()[2]
                elif len(prices) > 1:
                    print("more than 1 price")
                #print product_name + '\t' + price
                results.append(product_name + '\t' + price)
        else: 
            print("0 length")
        return results