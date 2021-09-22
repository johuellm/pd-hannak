from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class OfficeDepotParser(EcommerceParser):
    def __init__(self, html_file):
        super(OfficeDepotParser, self).__init__(html_file)    
        self.product_section_selector = ".product_block"    
        self.product_selector = ".item_sku [value]"
        self.price_selector = ".price_amount .hide"
        
        
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
                    product_name = products[0].value
                price = 'No price'
                if len(prices) == 1:
                    price = prices[0].text_content().strip()
                #print product_name #+ '\t' + price
                results.append(product_name + '\t' + price)

        return results