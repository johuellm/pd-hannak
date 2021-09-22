#!/usr/bin/env python

import sys, os, time
import hotel_tools as ht

datadir = 'hotels/'
plotdir = 'plots/'

#stores = ['hotels', 'expedia'] 
stores = ['expedia']

expedia_experiments = [('OS', 'win7'),('browser', 'firefox'),('OS', 'control')]

hotels_experiments = [('OS', 'win7'),('browser', 'firefox'),('OS', 'control')]

for hotel in stores:
    if hotel == 'expedia':
        experiments = expedia_experiments
    elif hotel == 'hotels':
        experiments = hotels_experiments

    out = open(os.path.join(plotdir, 'hotel_' + hotel + '_clear_cookies.txt'), 'w')
    i = 0

    for folder in os.listdir(os.path.join(datadir, hotel, 'logged_out')):
        timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
        
        
        print 'Running', hotel, folder
        
        for key in ht.keywords:
            i += 1
            
            # load the clear cookie data
            try:
                cpage = ht.parse(hotel, os.path.join(datadir, hotel, 'logged_out', folder, 'clear', key + '.html'))
            except:
                print "Can't find clear cookie data for", key
                out.write('%i %i\n' % (i, -1))
                continue
            if len(cpage) == 0:
                print "No clear cookie data for", key
                out.write('%i %i\n' % (i, -1))
                continue

            found = False
            miss = False
            for j in range(len(experiments)):
                exp, test = experiments[j]
                try:
                    tpage = ht.parse(hotel, os.path.join(datadir, hotel, exp, folder, test, key + '.html'))
                except:
                    print "Can't find test data for", key
                    miss = True
                    continue
                if len(tpage) == 0:
                    print "No test data for", key
                    miss = True
                    continue

                if ht.jaccard(cpage, tpage) > 0.94:
                    out.write('%i %i\n' % (i, j))
                    found = True
                    break

            if not found and not miss:
                out.write('%i %i\n' % (i, len(experiments)))
            else:
                out.write('%i %i\n' % (i, -1))


