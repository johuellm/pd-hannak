#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import hotel_tools as ht

datadir = 'hotels/'
procdir = 'processed/'
plotdir = 'plots/'

MIN_DATA = 75

stores = ['hotels', 'expedia', 'hotels_spend'] 

hotel_dir = 'browser'
expedia_controls = ('browser', 'ie8')
expedia_experiments = {
    'bucket_1' : ('OS', 'win7'),
    'bucket_2' : ('browser', 'firefox'),
    'bucket_3' : ('OS', 'control'),
}

hotels_controls = ('browser', 'ie8')
hotels_experiments = {
    'bucket_1' : ('OS', 'win7'),
    'bucket_2' : ('browser', 'firefox'),
    'bucket_3' : ('OS', 'control'),
}

spend_dir = 'spender'
hotel_spend_controls = ('spender', 'control')
hotel_spend_experiments = {
    'bucket_1' : ('spender', 'control2'),
    'bucket_2' : ('spender', 'buy_high'),
    'bucket_3' : ('spender', 'buy_low'),
}

for hotel in stores:
    outfiles = {}

    if hotel == 'expedia':
        root_dir = hotel_dir
        controls = expedia_controls
        experiments = expedia_experiments
    elif hotel == 'hotels':
        root_dir = hotel_dir
        controls = hotels_controls
        experiments = hotels_experiments
    elif hotel == 'hotels_spend':
        root_dir = spend_dir
        controls = hotels_spend_controls
        experiments = hotels_spend_experiments

    for test in experiments.iterkeys():
        outfiles[test] = open(os.path.join(procdir, 'hotel_' + hotel + '_' + test + '.txt'), 'w')
    day = 0

    for folder in os.listdir(os.path.join(datadir, hotel, root_dir)):
        timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
        
        print 'Running', hotel, folder
        
        # load the control data
        cpages = {}
        cexp, ctest = controls
        
        for key in ht.keywords:
            try:
                cpages[key] = ht.parse(hotel, os.path.join(datadir, hotel, cexp, folder, ctest, key + '.html'))
            except:
                print "Can't find control data for", key

        for test, pair in experiments.iteritems():
            cexp, ctest = pair
            j = []
            e = []
            k = []
            a = []
            c = 0
            d = []
            for key in ht.keywords:
                if key not in cpages: continue
                cpage = cpages[key]

                try:
                    tpage = ht.parse(hotel, os.path.join(datadir, hotel, cexp, folder, ctest, key + '.html'))
                except:
                    print "Can't find test data for", key
                    continue

                if len(cpage) == 0 or len(tpage) == 0: continue
                
                j.append(ht.jaccard(cpage, tpage))
                ed, kt = ht.editdist_and_kendalltau(cpage, tpage)
                e.append(ed)
                k.append(kt)
                a.append(ht.avg_page_price(tpage))
                common, dp = ht.different_prices(cpage, tpage)
                c += common
                d.extend(dp)
                
            out = outfiles[test]

            if len(j) == 0:
                print "No data in", folder
                out.write('%i %f 0 0 0 0 0 0 0 0 0 0 0 0\n' % (day, timestamp))
                continue

            if len(d) == 0:
                tmeand = 0
                tstdd = 0
            else:
                tmeand = tmean(d)
                tstdd = ht.safe_tstd(d)
            if c != 0: c = float(len(d))/c*100
                    
            out.write('%i %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % (day, timestamp, float(len(j))/len(ht.keywords)*100,
                                                                       tmean(j), ht.safe_tstd(j),
                                                                       tmean(e), ht.safe_tstd(e), tmean(k), ht.safe_tstd(k),
                                                                       tmean(a), ht.safe_tstd(a), c,
                                                                       tmeand, tstdd))
            out.flush()
        day += 1

# 0   1         2       3           4           5        6        7      8      9         10        11       12       13          
# day timestamp %_avail avg_jaccard std_jaccard avg_edit std_edit avg_kt std_kt avg_pdiff std_pdiff %_common avg_disc std_disc    

for hotel in stores:
    if hotel == 'expedia':
        experiments = expedia_experiments
    elif hotel == 'hotels':
        experiments = hotels_experiments

    for target in experiments.iterkeys():
        f = open(os.path.join(procdir, 'hotel_' + hotel + '_' + target + '.txt'))
        out = open(os.path.join(plotdir, 'hotel_' + hotel + '_' + target + '.txt'), 'w')
        for line in f:
            e = line.split()
            if float(e[2]) >= MIN_DATA: out.write(line)
