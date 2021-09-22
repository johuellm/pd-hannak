#!/usr/bin/env python

import os, subprocess

header = """load 'style3.gnu'

set xlabel "Day"
set xdata time
set timefmt "%s"
#set xrange ["03/21/95":"03/22/95"]
set xtics 604800
set format x "%m/%d"
"""
#set xtics (%s) 
#""" % (', '.join(['"' + str(x+1) + '" ' + str(x) for x in range(30)]))

hotel_tests = [('jaccard', 'bottom right', '[0:1]', 'Avg. Jaccard', '4', '5'),
               ('edit', 'top right', '', 'Avg. Edit Distance', '6', '7'),
               ('kt', 'bottom right', '[-1:1]', 'Avg. Kendall-Tau', '8', '9'),
               ('avgprice', 'bottom right', '', 'Avg. Total Price per Page', '10', '11'),
               ('diff', 'top right', '[0:10]', '% of Items w/ Diff. Prices', '12', None),
               ('pdiff', 'top right', '', 'Avg. Price Difference', '13', '14'),
]

hotels = ['cheaptickets', 'expedia', 'hotels', 'orbitz', 'priceline', 'travelocity', 'venere']
# 'booking', 'kayak',

car_tests = [('avgprice', 'bottom right', '', 'Avg. Price per Page', '4', '5'),
             ('diff', 'top right', '[0:10]', '% of Items w/ Diff. Prices', '6', None),
             ('pdiff', 'top right', '', 'Avg. Price Difference', '7', '8'),
]

cars = ['cheaptickets', 'expedia', 'orbitz', 'priceline', 'travelocity']

stores = ['bestbuy','cdw','homedepot','jcpenney','macys','newegg','officedepot','sears','staples','walmart']

experiments = {
    'browser': ['Chrome', 'IE8', 'Firefox', 'Safari'],
    'OS': ['Win7', 'XP', 'Linux', 'OSX'],
    'logged_out' : ['Out', 'In', 'Clear'],
}

hotels_experiments = {
    'bucket': ['Bucket 1', 'Bucket 2', 'Bucket 3'],
}
expedia_experiments = {
    'bucket': ['Bucket 1', 'Bucket 2', 'Bucket 3'],
}

spend_experiments = {
    'spender': ['control2', 'click_low', 'click_high', 'buy_low', 'buy_high'],
}

spend_h = ['expedia', 'hotels', 'priceline', 'travelocity']

plotdir = 'plots/'

def gen_gnuplots(prefix, stores, tests, experiments):
    for experiment in experiments.iterkeys():
        for test in tests:
            for hotel in stores:
                script = header
                script += 'set ylabel "' + test[3] + '"\n\n'
                
                if experiment != 'bucket': script += 'set output "plots/%s_%s_%s_%s.eps"\n' % (prefix, hotel, experiment, test[0])
                else: script += 'set output "plots/%s_%s_bucket_%s.eps"\n' % (prefix, hotel, test[0])

                script += 'set key ' + test[1] + '\n'
                if test[2]: script += 'set yrange ' + test[2] + '\n'
                script += '\nplot '

                first = experiments[experiment][0]
                last = experiments[experiment][-1]
                i = 1
                for target in experiments[experiment]:
                    if target != first: script += '\t'

                    if experiment != 'bucket': script += '"plots/%s_%s_%s_%s.txt" u 2:%s w lines t "%s' % (prefix, hotel, experiment,
                                                                                                           target.lower().replace(' ', '_'),
                                                                                                           test[4], target)
                    else: script += '"plots/%s_%s_%s.txt" u 2:%s w lines t "%s' % (prefix, hotel, target.lower().replace(' ', '_'),
                                                                                   test[4], target)

                    if target == first: script += '*'
                    script += '" ls %i' % (i)
                    i += 1
                    if target != last:
                        script += ',\\'
                    script += '\n'

                out = open('plots/%s_%s_%s_%s.plt' % (prefix, hotel, experiment, test[0]), 'w')
                out.write(script)
                out.close()

                p = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE)
                p.communicate(input=script)
                p.wait()

def gen_ndcg(prefix, stores, experiments):
    for experiment in experiments.iterkeys():
        fields = ['Control']
        fields.extend(experiments[experiment])

        for store in stores:
            script = header
            script += 'set ylabel "Avg. nDCG"\n\n'
            script += 'set output "plots/%s_%s_%s_ndcg.eps"\n' % (prefix, store, experiment)
            script += 'set key top right\nset yrange [0:1]\nset ytics 0.2\n\nplot '
            
            first = fields[0]
            last = fields[-1]
            for i, field in enumerate(fields):
                if field != first:
                    script += '\t'
                script += '"plots/%s_%s_%s_ndcg.txt" u 2:%i w lines t "%s" ls %i' % (prefix, store, experiment, 2 * i + 3,
                                                                                     field, i + 1)
                if field != last:
                    script += ',\\'
                script += '\n'

            out = open('plots/%s_%s_%s_ndcg.plt' % (prefix, store, experiment), 'w')
            out.write(script)
            out.close()

            p = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE)
            p.communicate(input=script)
            p.wait()
    

# basic plots for hotels, ecommerce, and cars
gen_gnuplots("hotel", hotels, hotel_tests, experiments)
gen_ndcg("hotel", hotels, experiments)

gen_gnuplots("ecommerce", stores, hotel_tests, experiments)
gen_ndcg("ecommerce", stores, experiments)

gen_gnuplots("car", cars, car_tests, experiments)

# plots for the spender tests on hotels and cars
gen_gnuplots("hotel", spend_h, hotel_tests, spend_experiments)
gen_ndcg("hotel", spend_h, spend_experiments)

gen_gnuplots("car", cars, car_tests, spend_experiments)

# plots for bucketized hotel sites
gen_gnuplots("hotel", ['hotels'], hotel_tests, hotels_experiments)
gen_ndcg("hotel", ['hotels'], hotels_experiments)

gen_gnuplots("hotel", ['expedia'], hotel_tests, expedia_experiments)
gen_ndcg("hotel", ['expedia'], expedia_experiments)

# normal ads on hotels
gen_gnuplots("hotel_ads", hotels, hotel_tests, experiments)
gen_gnuplots("hotel_ads", spend_h, hotel_tests, spend_experiments)

# ads on bucketized hotel sites
gen_gnuplots("hotel_ads", ['hotels'], hotel_tests, hotels_experiments)
gen_gnuplots("hotel_ads", ['expedia'], hotel_tests, expedia_experiments)
