#!/usr/bin/env python

import sys, os, time
from scipy.stats import tmean
import ecommerce_tools as et

datadir = 'ecommerce\\'
procdir = 'processed/'
if not os.path.exists(procdir):
    os.makedirs(procdir)
plotdir = 'plots/'
if not os.path.exists(plotdir):
    os.makedirs(plotdir)

MIN_DATA = 50

#stores = ['bestbuy','cdw','homedepot','jcpenney','macys','newegg','officedepot','sears','staples','walmart']
stores = ['local']

experiments = {
    'browser': ['chrome', 'ie8', 'firefox', 'safari', 'safari_osx', 'android'],
    'OS': ['win7', 'xp', 'linux', 'osx'],
#    'logged_out' : ['in', 'out', 'clear'],
}

for store in stores:
    #print(experiments.keys())
    for experiment in experiments.keys():
        outfiles = {}
        for test in experiments[experiment]:
            outfiles[test] = open(os.path.join(procdir, 'ecommerce_' + store + '_' + experiment + '_' + test + '.txt'), 'w')
        day = 0

        for folder in os.listdir(os.path.join(datadir, store, experiment)):
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
            print('Running', store, experiment, folder)

            # load the control data
            cpages = {}
            for key in et.keywords[store]:
                #print(os.path.join(datadir, store, experiment, folder, et.control, key + '.html'))
                try:
                    #print(f"store: {store}")
                    cpage = et.parse(store, os.path.join(datadir, store, experiment, folder, et.control, key + '.html'))
                    #print(f"cpage: {cpage}")
                except IOError:
                    print("Can't find control data for", key)
                    continue
                if len(cpage) < 3:
                    print("Control data is empty for", key)
                    continue
                cpages[key] = cpage

            #print(f"experiments: {experiments}")
            for test in experiments[experiment]:
                j = []
                e = []
                k = []
                a = []
                c = 0
                d = []
                #print(et.keywords[store])
                for key in et.keywords[store]:
                    if key not in cpages: continue
                    cpage = cpages[key]

                    try:
                        tpage = et.parse(store, os.path.join(datadir, store, experiment, folder, test, key + '.html'))
                    except IOError:
                        print("Can't find test data for", key)
                        continue

                    #print(tpage)
                    if len(tpage) < 3:
                        print("Test data is empty for", key)
                        continue

                    #print(j, et.jaccard(cpage, tpage))

                    j.append(et.jaccard(cpage, tpage))
                    ed, kt = et.editdist_and_kendalltau(cpage, tpage)
                    e.append(ed)
                    k.append(kt)
                    a.append(et.avg_page_price(tpage))
                    common, dp = et.different_prices(cpage, tpage)
                    c += common
                    d.extend(dp)

                out = outfiles[test]

                if len(j) == 0:
                    print("No data for", experiment, 'in', folder)
                    out.write('%i %f 0 0 0 0 0 0 0 0 0 0 0 0\n' % (day, timestamp))
                    continue

                if len(d) == 0:
                    tmeand = 0
                    tstdd = 0
                else:
                    tmeand = tmean(d)
                    tstdd = et.safe_tstd(d)
                if c != 0: c = float(len(d))/c*100

                out.write(' %i %f %f %f %f %f %f %f %f %f %f %f %f %f\n' % (day, timestamp, float(len(j))/len(et.keywords[store])*100,
                                                                               tmean(j), et.safe_tstd(j),
                                                                               tmean(e), et.safe_tstd(e), tmean(k), et.safe_tstd(k),
                                                                               tmean(a), et.safe_tstd(a), c,
                                                                               tmeand, tstdd))
                out.flush()
            day += 1

# 0   1         2       3           4           5        6        7      8      9         10        11       12       13          
# day timestamp %_avail avg_jaccard std_jaccard avg_edit std_edit avg_kt std_kt avg_pdiff std_pdiff %_common avg_disc std_disc    

for store in stores:
    for experiment in experiments.keys():
        for target in experiments[experiment]:
            f = open(os.path.join(procdir, 'ecommerce_' + store + '_' + experiment + '_' + target + '.txt'))
            out = open(os.path.join(plotdir, 'ecommerce_' + store + '_' + experiment + '_' + target + '.txt'), 'w')
            for i, line in enumerate(f):
                e = line.split()
                if float(e[2]) >= MIN_DATA: out.write(line)
