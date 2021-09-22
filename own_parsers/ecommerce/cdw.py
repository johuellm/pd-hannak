from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class CdwParser(EcommerceParser):
    def __init__(self, html_file):
        super(CdwParser, self).__init__(html_file)    
        self.product_section_selector = ".searchrow"    
        self.product_selector = ".searchrow-description [id$='hprProductLink']"
        self.price_selector = ".searchrow-price .selected-price.price"
        #self.sku_selector = ".attributes strong[class=sku]"
#         self.product_section_selector2 = ".searchrow"
#         self.product_selector2 = ".searchrow-description [id$='hprProductLink']"
#         self.price_selector2 = ".searchrow-price .selected-price.price"
#         
        
    def parse_list(self):
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        
        #skus = self.root.cssselect(self.sku_selector)
        if len(product_sections) != 0:
            products = self.root.cssselect(self.product_selector)
            prices = self.root.cssselect(self.price_selector)
            for product_section in product_sections:
                #print "psection:  " + str(product_section)
                products = product_section.cssselect(self.product_selector)
                prices = product_section.cssselect(self.price_selector)
                #skus = self.root.cssselect(self.sku_selector)
                product_name = ''
                #print products 
                if len(products) == 1:
                    product_name = products[0].text_content().strip()

                if '\n' in product_name: product_name = product_name.split('\n')[0].strip()

                price = 'No price'
                if len(prices) == 1:
                    price = prices[0].text_content().strip()

                if price == 'Call': price = 'No price'

                results.append(product_name + '\t' + price)
#         else:
#             product_sections = self.root.cssselect(self.product_section_selector2)
#             products = self.root.cssselect(self.product_selector2)
#             prices = self.root.cssselect(self.price_selector2)
            
        return results
