from own_parsers.ecommerce.all_ecommerce import EcommerceParser
import lxml.html
import sys

class HomeDepotParser(EcommerceParser):
    def __init__(self, html_file):
        super(HomeDepotParser, self).__init__(html_file)    
        self.product_section_selector = ".cell_section2"
        self.product_selector = ".item_description"     #".model_container"
        self.ios_product_selector = ".normal.item-description"
        self.android_product_selector = ".product.normal"
        self.price_selector = ".item_pricing_wrapper"
        self.ios_price_selector = ".xlarge.item-price"
        self.android_price_selector = ".price.large.bold"
        
    def parse_list(self):
        results = []
        product_sections = self.root.cssselect(self.product_section_selector)
        
        #skus = self.root.cssselect(self.sku_selector)
        if len(product_sections) != 0:
            #products = self.root.cssselect(self.product_selector)
            #prices = self.root.cssselect(self.price_selector)
            for product_section in product_sections:
                products = product_section.cssselect(self.product_selector)
                prices = product_section.cssselect(self.price_selector)
                product_name = ''
                #print products 
                if len(products) == 1:
                    product_name = products[0].text_content().split('\n')[1].strip()
                price = 'No price'
                #if len(prices) == 1:
                
                # Christo's fixes for extra crap in prices
                price = prices[0].text_content().split()[0]
                price = price.split('/')[0].strip()
                                
                #print product_name + '\t' + price
                results.append(product_name + '\t' + price)
        else:
            products = self.root.cssselect(self.ios_product_selector)
            prices = self.root.cssselect(self.ios_price_selector)

            if len(products) == 0:
                products = self.root.cssselect(self.android_product_selector)
                prices = self.root.cssselect(self.android_price_selector)

            for prod, price in zip(products, prices):
                product_name = prod.text_content().split('\n')[2].strip()
                p = price.text_content().split()[0]
                p = p.split('/')[0].strip()
                results.append(product_name + '\t' + p)                

        #else: 
        #    print "0 length", self.html_file
        return results
