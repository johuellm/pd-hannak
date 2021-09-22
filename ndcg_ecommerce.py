#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import ecommerce_tools as et

datadir = 'ecommerce/'
plotdir = 'plots/'

MIN_DATA = 50

#stores = ['bestbuy','cdw','homedepot','jcpenney','macys','newegg','officedepot','sears','staples','walmart']
stores = ['local']

experiments = {
    'browser': ['chrome', 'ie8', 'firefox', 'safari'],
    'OS': ['win7', 'xp', 'linux', 'osx'],
#    'logged_out' : ['out', 'in', 'clear'],
}

extra_browsers = ['safari_osx', 'android']

for store in stores:
    for experiment in experiments.keys():
        short_fields = [et.control]
        short_fields.extend(experiments[experiment])

        out = open(os.path.join(plotdir, 'ecommerce_' + store + '_' + experiment + '_ndcg.txt'), 'w')
        out.write('#')
        for field in short_fields:
            out.write(' %s' % field)
        out.write('\n')

        if experiment == 'browser':
            long_fields = short_fields[:]
            long_fields.extend(extra_browsers)

            out2 = open(os.path.join(plotdir, 'ecommerce_' + store + '_' + experiment + '2_ndcg.txt'), 'w')
            out2.write('#')
            for field in extra_browsers:
                out2.write(' %s' % field)
            out2.write('\n')

        day = 0

        for folder in os.listdir(os.path.join(datadir, store, experiment)):
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
            #print 'Running', store, experiment, folder

            ndcg = []
            for key in et.keywords[store]:
                pages = []
                skip = False
                fields = short_fields
                if experiment == 'browser' and timestamp > 1398312000: # 4/24/2014
                    print('Using extended browsers')
                    fields = long_fields
                for field in fields:
                    try:
                        page = et.parse(store, os.path.join(datadir, store, experiment, folder, field, key + '.html'))
                    except:
                        print("Can't find test data for", store, experiment, folder, field, key)
                        skip = True
                        break

                    if len(page) < 3:
                        print("No results for", store, experiment, folder, field, key)
                        skip = True
                        break

                    pages.append(page)

                if not skip:
                    ndcg.append(et.ndcg(pages))

            if float(len(ndcg))/len(et.keywords[store])*100 < MIN_DATA:
                continue

            out.write('%i %f' % (day, timestamp))

            for i, field in enumerate(short_fields):
                l = []
                for a in ndcg:
                    l.append(a[i])
                out.write(' %f %f' % (tmean(l), et.safe_tstd(l)))
            out.write('\n')

            if experiment == 'browser' and timestamp > 1398312000: # 4/24/2014
                print('Writing extended browsers')
                out2.write('%i %f' % (day, timestamp))

                for i, field in enumerate(extra_browsers):
                    i += len(short_fields)
                    l = []
                    for a in ndcg:
                        l.append(a[i])
                    out2.write(' %f %f' % (tmean(l), et.safe_tstd(l)))
                out2.write('\n')

            day += 1

