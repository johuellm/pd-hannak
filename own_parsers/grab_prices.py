import os
import sys
import subprocess
import platform

working_dir = '' # this is the directory where the html files are stored
results_dir = '' # this is the directory where the output will go
connector = '' 
site_type = 'hotel_parser.py'
to_parse = [ 'baseline1_pd', 'baseline2_pd', 'received_data'] # experiment type to parse
to_ignore = ['own_parsers.py', 'error.txt', '.DS_Store', 'formats', 'grab_prices.py', 'html.png', 'ip_achtung', 'own_parsers.js', 'trial1.txt']
to_check = [ 'priceline', 'expedia', 'cheaptickets', 'orbitz', 'travelocity'] # stores to parse

# used to count how many of each site were parsed
stats = {} 
final_stats = {}

# looks at the args to see what to parse
if len(sys.argv) == 2:
	if sys.argv[1] == 'car':
		site_type = 'car/own_parsers.py'
	elif sys.argv[1] == 'hotel':
		site_type = 'hotel/own_parsers.py'
	else:
		print 'unknown own_parsers'
		exit()

min_file_size = 0


def add_site(company):
	if company in stats:
		stats[company] += 1
	else:
		stats[company] = 1

def add_final_site(company):
	if company in final_stats:
		final_stats[company] += 1
	else:
		final_stats[company] = 1

def count_site(my_file):
	for site in to_check:
		if site in my_file:
			add_final_site(site)


def count_files(directory):
	files = os.listdir(directory)
	for f in files:
		count_site(f)

def get_stats():
	folders = os.listdir(results_dir)
	for output_folder in folders:
		if output_folder in to_parse:
			count_files(results_dir + '/' + output_folder)

def loop_through_tests():
	for folder in to_parse:
		temp_dir = working_dir + connector + folder
		if os.path.isdir(temp_dir):
			loop_through_ip(temp_dir, folder)
		else:
			print "Not a valid directory\t" + temp_dir


def loop_through_ip(curr_dir, test):
	folders = os.listdir(curr_dir)
	for folder in folders:
		if(folder not in to_ignore):
			ip_dir = curr_dir + "/" + folder 
			loop_through_companies(ip_dir, test, folder)

def loop_through_companies(ip_dir, test, ip):
	companies = os.listdir(ip_dir)
	for company in companies:
		if company in to_check:
			company_dir = ip_dir + "/" + company
			loop_through_files(company_dir, company, test, ip)

def loop_through_files(company_dir, company, test, ip):
	files = os.listdir(company_dir)
	for f in files:
		if '.html' in f and os.path.getsize(company_dir + "/" + f) > min_file_size:
			temp_html_file = company_dir + "/" + f
			output_file = results_dir + "/" + test + '/' + ip + '_' + company + '.txt'
			add_site(company)
			p = subprocess.call(["python", site_type, company, temp_html_file, output_file, 'experiment'])

def print_stats():
	print 'Site\t\tAttempted\t\tFound'
	for site in stats:
		print site + '\t\t' + str(stats[site]) + '\t\t' + str(final_stats[site])


loop_through_tests()
get_stats()
print_stats()


