# There are usually 3 ads on the page, 1 on top, two at the bottom

from hotel import HotelParser

class TravelocityAdParser(HotelParser):

	def __init__(self, html_file):
		super(TravelocityAdParser, self).__init__(html_file)
		self.article_selector = 'article.segment.hotel.avgPerNight.travelAd'
		self.hotel_name_selector = 'span.hotelName strong' #'.module .object .view .property-name'
		self.price_selector = 'span.actualPrice' #'.module .object .view .pricing-info .price'
		self.city_selector = ''
		self.date_selector = '.header .content .brief .first'

	def parse_date(self):
		try:
			date = self.root.cssselect(self.date_selector)[0].text_content().strip()
			if date == 'Tue, Jan 7, 2014 - Fri, Jan 10, 2014':
				return 'A'
			elif date == 'Fri, Dec 27, 2013 - Sat, Jan 4, 2014':
				return 'B'
			elif date == 'Fri, May 9, 2014 - Sat, May 17, 2014':
				return 'C'
		except:
			pass
		return 'Z'

	def parse_hotels(self):
		acc = []
		for article in self.articles:
			acc.append(article.cssselect(self.hotel_name_selector)[0].text_content().strip())
		return acc
	
	def parse_prices(self):
		self.articles = self.root.cssselect(self.article_selector)
		acc = []
		for article in self.articles:
			price = article.cssselect(self.price_selector)[0].text_content().strip().replace('$', '')
			if price == '':
				acc.append('No Results')
			else:
				acc.append(price)
		return acc

	
