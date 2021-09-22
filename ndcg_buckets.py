#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import hotel_tools as ht

datadir = 'hotels/'
plotdir = 'plots/'

MIN_DATA = 75

stores = ['expedia', 'hotels']

expedia_fields = ['control', 'bucket_1', 'bucket_2', 'bucket_3']
expedia_experiments = {
    'control' : ('browser', 'ie8'),
    'bucket_1' : ('OS', 'win7'),
    'bucket_2' : ('browser', 'firefox'),
    'bucket_3' : ('OS', 'control'),
}

hotels_fields = ['control', 'bucket_1', 'bucket_2', 'bucket_3']
hotels_experiments = {
    'control' : ('browser', 'ie8'),
    'bucket_1' : ('OS', 'win7'),
    'bucket_2' : ('browser', 'firefox'),
    'bucket_3' : ('OS', 'control'),
}

for hotel in stores:
    if hotel == 'expedia':
        experiments = expedia_experiments
        fields = expedia_fields
    elif hotel == 'hotels':
        experiments = hotels_experiments
        fields = hotels_fields

    out = open(os.path.join(plotdir, 'hotel_' + hotel + '_bucket_ndcg.txt'), 'w')
    out.write('#')
    for field in fields:
        out.write(' %s' % field)
    out.write('\n')

    day = 0

    for folder in os.listdir(os.path.join(datadir, hotel, 'browser')):
        timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
        print 'Running', hotel, folder

        ndcg = []
        for key in ht.keywords:
            pages = []
            skip = False
            for field in fields:
                cexp, ctest = experiments[field]
                try:
                    page = ht.parse(hotel, os.path.join(datadir, hotel, cexp, folder, ctest, key + '.html'))
                except:
                    print "Can't find test data for", key
                    skip = True
                    break

                if len(page) == 0:
                    skip = True
                    break

                pages.append(page)

            if not skip: ndcg.append(ht.ndcg(pages))
            
        if float(len(ndcg))/len(ht.keywords)*100 < MIN_DATA: continue

        out.write('%i %f' % (day, timestamp))

        for i, field in enumerate(fields):
            l = []
            for a in ndcg:
                l.append(a[i])
            out.write(' %f %f' % (tmean(l), ht.safe_tstd(l)))
        out.write('\n')

        day += 1

