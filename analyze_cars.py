#!/usr/bin/env python

import sys, os, time
import car_tools as ct
from scipy.stats import tmean

datadir = 'cars/'
procdir = 'processed/'
plotdir = 'plots/'

MIN_DATA = 55

stores = ['priceline', 'cheaptickets', 'expedia', 'orbitz', 'travelocity']

experiments = {
    'browser': ['chrome', 'ie8', 'firefox', 'safari', 'safari_osx', 'android'],
    'OS': ['win7', 'xp', 'linux', 'osx'],
    'logged_out' : ['in', 'out', 'clear'],
    'spender': ['control2', 'click_low', 'click_high', 'buy_low', 'buy_high'],
}

for car in stores:
    for experiment in experiments.iterkeys():        
        outfiles = {}
        for test in experiments[experiment]:
            outfiles[test] = open(os.path.join(procdir, 'car_' + car + '_' + experiment + '_' + test + '.txt'), 'w')
        day = 0

        for folder in os.listdir(os.path.join(datadir, car, experiment)):
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            
            print 'Running', car, experiment, folder

            # load the control data
            cpages = {}
            for key in ct.keywords:
                try:
                    cpages[key] = ct.parse(car, os.path.join(datadir, car, experiment, folder, ct.control, key + '.html'))
                except:
                    print "Can't find control data for", key

            for test in experiments[experiment]:
                a = []
                c = 0
                d = []
                for key in ct.keywords:
                    if key not in cpages: continue
                    cpage = cpages[key]

                    try:
                        tpage = ct.parse(car, os.path.join(datadir, car, experiment, folder, test, key + '.html'))
                    except:
                        print "Can't find test data for", key
                        continue

                    if len(cpage) == 0 or len(tpage) == 0: continue

                    a.append(ct.avg_page_price(tpage))
                    common, dp = ct.different_prices(cpage, tpage)
                    c += common
                    d.extend(dp)

                out = outfiles[test]

                if len(a) == 0:
                    print "No data for", experiment, 'in', folder
                    out.write('%i %f 0 0 0 0 0\n' % (day, timestamp))
                    continue

                if len(d) == 0:
                    tmeand = 0
                    tstdd = 0
                else:
                    tmeand = tmean(d)
                    tstdd = ct.safe_tstd(d)
                if c != 0: c = float(len(d))/c*100
                    
                out.write('%i %f %f %f %f %f %f %f\n' % (day, timestamp, float(len(a))/len(ct.keywords)*100,
                                                         tmean(a), ct.safe_tstd(a), c,
                                                         tmeand, tstdd))
                out.flush()
            day += 1

# 0   1         2       3         4         5        6        7
# day timestamp %_avail avg_pdiff std_pdiff %_common avg_disc std_disc    

for car in stores:
    for experiment in experiments.iterkeys():
        for target in experiments[experiment]:
            f = open(os.path.join(procdir, 'car_' + car + '_' + experiment + '_' + target + '.txt'))
            out = open(os.path.join(plotdir, 'car_' + car + '_' + experiment + '_' + target + '.txt'), 'w')
            for line in f:
                e = line.split()
                if float(e[2]) >= MIN_DATA: out.write(line)
