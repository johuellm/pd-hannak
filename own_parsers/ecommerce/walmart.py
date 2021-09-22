from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html

class WalmartParser(EcommerceParser):
    def __init__(self, html_file):
        super(WalmartParser, self).__init__(html_file)    
        self.product_section_selector = ".item.item-general-view"    
        self.product_selector = ".prodLink.GridItemLink"
        self.price_selector = ".item.item-general-view .camelPrice .bigPriceText2"
        
        
    def parse_list(self):
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        
        #skus = self.root.cssselect(self.sku_selector)
        if len(product_sections) != 0:
            products = self.root.cssselect(self.product_selector)
            prices = self.root.cssselect(self.price_selector)
            for product_section in product_sections:
                #print "psection:  " + str(product_section)
                html = lxml.html.fromstring(lxml.html.tostring(product_section))
                #print '*******'  
                #print html
                products = html.cssselect(self.product_selector)
                prices = html.cssselect(self.price_selector)
                product_name = ''
                #print products 
                if len(products) == 1:
                    product_name = products[0].text_content().strip()
                    #print product_name
                price = 'No price'
                if len(prices) > 0:
                    price = prices[0].text_content() #.strip()
                #print product_name + '\t' + price
                results.append(product_name + '\t' + price)
#         else:
#             product_sections = self.root.cssselect(self.product_section_selector2)
#             products = self.root.cssselect(self.product_selector2)
#             prices = self.root.cssselect(self.price_selector2)
            
        return results