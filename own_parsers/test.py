#!/usr/bin/python
import sys
import os
import filecmp
import subprocess

'''
Written by Gary Soeller

This is the test script for all the parsers
In order to run, execute ./test.py 
This will run all the tests. If you want to run a specific
test, then add any of the args ['hotel', 'merchant', 'car']
'''

# sites to test
to_test = ['orbitz', 'expedia', 'cheaptickets', 'priceline', 'priceline_list', 'travelocity', 'hotels', 'venere']
#to_test = ['cheaptickets']

# scripts to test
merchant_script = os.getcwd() + '/' + 'merchant_parser.py'
car_script = os.getcwd() + '/' + 'car_parser.py'
hotel_script = os.getcwd() + '/' + 'hotel_parser.py'

# location of html files
hotel_test_dir = os.getcwd() + '/' + 'test_files' + '/' + 'hotel'
car_test_dir = os.getcwd() + '/' + 'test_files' + '/' + 'car'
merchant_test_dir = os.getcwd() + '/' + 'test_files' + '/' + 'merchant'

print car_script
print hotel_script
print merchant_script

test_merchants = False
test_hotels = False
test_cars = False

if len(sys.argv) == 1:
	test_merchants = True
	test_hotels = True
	test_cars = True

elif len(sys.argv) > 1 and len(sys.argv) < 5:
	if 'merchant' in sys.argv:
		test_merchants = True
	if 'hotel' in sys.argv:
		test_hotels = True
	if 'car' in sys.argv:
		test_cars = True

else:
	print 'Too many arguments'
	exit()

# gets the result file for the dir and store
def get_result_file(store, my_dir):
	files = os.listdir(my_dir)
	for f in files:
		f = f[:-4]
		if store + '_result' == f:
			return f + '.txt'
	return None

def compare_files(f1, f2):
	f1 = open(f1, 'r')
	f2 = open(f2, 'r')
	if f1.read() == f2.read():
		f1.close()
		f2.close()
		return True
	f1.close()
	f2.close()
	return False



def valid_site(site):
	for page in to_test:
		if site in page or page in site:
			return True
	return False

# clears the test file	
def clear_test_file(test):
	if test == 'car':
		my_dir = car_test_dir
	elif test == 'hotel':
		my_dir = hotel_test_dir
	f = open(my_dir + '/temp_output12345.txt', 'w')
	f.write('')
	f.close()

# run tests for all the hotel sites
def testHotels():
	print 'Testing hotels'
	clear_test_file('hotel')
	files = os.listdir(hotel_test_dir)
	failed = False
	for f in files:
		if '.html' in f and valid_site(f):
			store = f.split('.')[0]
			result = hotel_test_dir + '/' + get_result_file(store, hotel_test_dir)
			temp = hotel_test_dir + '/temp_output12345.txt'
			f = hotel_test_dir + '/' + f 
			open(temp, 'a').close()
			store = store.replace('_list', '')
			p = subprocess.call(["python", "hotel/own_parsers.py", store, f, temp, 'test'])
			result = compare_files(result, temp)
			if result:
				result = 'PASS'
				clear_test_file('hotel')
			else:
				result = 'FAIL'
				failed = True
			print store + '\t......................\t' + '[' + result + ']'
			if failed:
				exit()

# run the tests for all the car sites
def testCars():
	print 'Testing Cars'
	clear_test_file('car')
	files = os.listdir(car_test_dir)
	failed = False
	for f in files:		
		if '.html' in f and valid_site(f):
			store = f.split('.')[0]
			result = car_test_dir + '/' + get_result_file(store, car_test_dir)
			#print result
			temp = car_test_dir + '/temp_output12345.txt'
			f = car_test_dir + '/' + f
			open(temp, 'a').close()
			#output = os.getcwd() + '/output_test.txt'
			#out = open(output)
			store = store.replace('_list', '')
			#print 'parsing\t' + store
			p = subprocess.call(["python", 'car/own_parsers.py', store, f, temp, 'test'])
			result = compare_files(result, temp)
			if result:
				result = 'PASS'
				clear_test_file('car')
			else:
				result = 'FAIL'
				failed = True

			print store + '\t......................\t' + '[' + result + ']'
			if failed:
				exit()
		
# run the tests for all the merchant sites
def testMerchants():
	print 'Testing Merchants'


# run the tests
if test_hotels:
	testHotels()
if test_cars:
	testCars()
if test_merchants:
	testMerchants()