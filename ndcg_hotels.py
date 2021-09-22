#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import hotel_tools as ht

datadir = 'hotels/'
plotdir = 'plots/'

MIN_DATA = 50

#stores = ['cheaptickets', 'expedia', 'hotels', 'orbitz', 'priceline',
#          'travelocity', 'venere'] # 'booking', 'kayak',
stores = ['hotels', 'priceline']

experiments = {
#    'browser': ['chrome', 'ie8', 'firefox', 'safari'],
#    'OS': ['win7', 'xp', 'linux', 'osx'],
#    'logged_out' : ['out', 'in', 'clear'],
    'spender': ['control2', 'click_low', 'click_high', 'buy_low', 'buy_high'],
}

extra_browsers = ['safari_osx', 'android']

for hotel in stores:
    for experiment in experiments.iterkeys():
        try:
            folder_list = os.listdir(os.path.join(datadir, hotel, experiment))
        except:
            print 'No folder for', hotel, 'and', experiment
            continue

        short_fields = [ht.control]
        short_fields.extend(experiments[experiment])

        out = open(os.path.join(plotdir, 'hotel_' + hotel + '_' + experiment + '_ndcg.txt'), 'w')
        out.write('#')
        for field in short_fields:
            out.write(' %s' % field)
        out.write('\n')

        if experiment == 'browser':
            long_fields = short_fields[:]
            long_fields.extend(extra_browsers)

            out2 = open(os.path.join(plotdir, 'hotel_' + hotel + '_' + experiment + '2_ndcg.txt'), 'w')
            out2.write('#')
            for field in extra_browsers:
                out2.write(' %s' % field)
            out2.write('\n')

        day = 0

        for folder in folder_list:
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
            print 'Running', hotel, experiment, folder

            ndcg = []
            for key in ht.keywords:
                pages = []
                skip = False
                fields = short_fields
                if experiment == 'browser' and timestamp > 1398312000: # 4/24/2014
                    print 'Using extended browsers'
                    fields = long_fields
                for field in fields:
                    try:
                        page = ht.parse(hotel, os.path.join(datadir, hotel, experiment, folder, field, key + '.html'))
                    except:
                        #print "Can't find test data for", key
                        skip = True
                        break

                    if len(page) == 0:
                        skip = True
                        break

                    pages.append(page)

                if not skip: ndcg.append(ht.ndcg(pages))

            if float(len(ndcg))/len(ht.keywords)*100 < MIN_DATA: continue

            out.write('%i %f' % (day, timestamp))

            for i, field in enumerate(short_fields):
                l = []
                for a in ndcg:
                    l.append(a[i])
                out.write(' %f %f' % (tmean(l), ht.safe_tstd(l)))
            out.write('\n')

            if experiment == 'browser' and timestamp > 1398312000: # 4/24/2014
                print 'Writing extended browsers'
                out2.write('%i %f' % (day, timestamp))

                for i, field in enumerate(extra_browsers):
                    i += len(short_fields)
                    l = []
                    for a in ndcg:
                        l.append(a[i])
                    out2.write(' %f %f' % (tmean(l), ht.safe_tstd(l)))
                out2.write('\n')

            day += 1

