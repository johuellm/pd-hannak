#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import hotel_tools as ht

datadir = 'hotels/'
procdir = 'processed/'
plotdir = 'plots/'

MIN_DATA = 40

#stores = ['cheaptickets', 'expedia', 'hotels', 'orbitz', 'priceline','travelocity']
stores = ['priceline']

experiments = {
#    'browser': ['chrome', 'ie8', 'firefox', 'safari', 'safari_osx', 'android'],
#    'OS': ['win7', 'xp', 'linux', 'osx'],
#    'logged_out' : ['in', 'out', 'clear'],
    'spender': ['control2', 'click_low', 'click_high', 'buy_low', 'buy_high'],
}

for hotel in stores:
    for experiment in experiments.iterkeys():        
        try:
            folder_list = os.listdir(os.path.join(datadir, hotel, experiment))
        except:
            print 'No folder for', hotel, 'and', experiment
            continue

        outfiles = {}
        for test in experiments[experiment]:
            print os.path.join(procdir, 'hotel_ads_' + hotel + '_' + experiment + '_' + test + '.txt')
            outfiles[test] = open(os.path.join(procdir, 'hotel_ads_' + hotel + '_' + experiment + '_' + test + '.txt'), 'w')
        day = 0

        for folder in folder_list:
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
            print 'Running', hotel, experiment, folder

            # load the control data
            cpages = {}
            for key in ht.keywords:
                try:
                    cpages[key] = ht.parse_ads(hotel, os.path.join(datadir, hotel, experiment, folder, ht.control, key + '.html'))
                except:
                    print "Can't find control data for", key

            for test in experiments[experiment]:
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
                        tpage = ht.parse_ads(hotel, os.path.join(datadir, hotel, experiment, folder, test, key + '.html'))
                    except:
                        print "Can't find test data for", key
                        continue

                    if len(cpage) == 0 or len(tpage) == 0: continue

                    j.append(ht.jaccard(cpage, tpage))
                    try:
                        ed, kt = ht.editdist_and_kendalltau(cpage, tpage)
                    except:
                        ed = 0
                        kt = 1
                    e.append(ed)
                    k.append(kt)
                    a.append(ht.avg_page_price(tpage))
                    common, dp = ht.different_prices(cpage, tpage)
                    c += common
                    d.extend(dp)

                out = outfiles[test]
                
                if len(j) == 0:
                    print "No data for", experiment, 'in', folder
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
    for experiment in experiments.iterkeys():
        min_data = MIN_DATA
        if hotel == 'priceline' and experiment == 'spender': min_data = 20;

        for target in experiments[experiment]:

            try:
                f = open(os.path.join(procdir, 'hotel_ads_' + hotel + '_' + experiment + '_' + target + '.txt'))
            except:
                print 'Missing', os.path.join(procdir, 'hotel_ads_' + hotel + '_' + experiment + '_' + target + '.txt')
                continue
            out = open(os.path.join(plotdir, 'hotel_ads_' + hotel + '_' + experiment + '_' + target + '.txt'), 'w')

            for line in f:
                e = line.split()
                if float(e[2]) >= min_data: out.write(line)
