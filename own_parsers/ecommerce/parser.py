import lxml.etree
import lxml.html
import sys
import datetime
import codecs
import inspect
import json

from bestbuy import BestBuyParser
from cdw import CdwParser
from jcpenney import JCPenneyParser
from walmart import WalmartParser
from officedepot import OfficeDepotParser
from staples import StaplesParser
from homedepot import HomeDepotParser
from macys import MacysParser
from sears import SearsParser
from local import LocalParser


error_file = 'error_ecommerce.txt'
output_file = ''



def log(message):
	# logs messages if running in production
	if sys.argv[3] == 'test':
		pass
	else:
		print(message)

def printParsed(parsed, html_file):
	if parsed == None:
		log('An error occurred parsing file:\t' + html_file)
	else:
		try:
			f = open(output_file, 'w')
			f.write(parsed.encode('utf-8'))
			if len(parsed) == 0:
				print(html_file)
			f.close()
			#log('success')
		except Exception as e:
			log(e)



def parseFile(html_file, error_file, store):
	parsed = {}

	if store == 'bestbuy':
		parser = BestBuyParser(html_file)
	if store == 'cdw':
		parser = CdwParser(html_file)
	if store == 'jcp':
		parser = JCPenneyParser(html_file)

	if store == 'walmart':
		parser = WalmartParser(html_file)
	if store == 'officedepot':
		parser = OfficeDepotParser(html_file)
	if store == 'staples':
		parser = StaplesParser(html_file)
	if store == 'homedepot':
		parser = HomeDepotParser(html_file)
	if store == 'macys':
		parser = MacysParser(html_file)
	if store == 'walmart':
		parser = WalmartParser(html_file)
	if store == 'sears':
		parser = SearsParser(html_file)
	if store == 'local':
		parser = LocalParser(html_file)
	return parser.parse()
	

#log(sys.argv)
if len(sys.argv) < 4:
	log("Error: Too few arguments")
	exit()

store_name = sys.argv[1]
html_file = sys.argv[2] 
output_file = sys.argv[3]

parsed = parseFile(html_file, error_file, store_name)
printParsed(parsed, html_file)

