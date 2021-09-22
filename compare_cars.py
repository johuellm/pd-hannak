#!/usr/bin/env python

import sys
from scipy.stats import tmean
import car_tools as ct

if len(sys.argv) < 3:
    print 'Usage: # ', sys.argv[0], '<car> <page 1> <page 2>'
    sys.exit()

page1 = ct.parse(sys.argv[1], sys.argv[2])
page2 = ct.parse(sys.argv[1], sys.argv[3])

l = max(len(page1), len(page2))
i = 0
while i < l:
    if i < len(page1): print '%20s\t%25s\t%.0f' % (page1[i][0][0:20], page1[i][1][0:25], page1[i][2]),
    else: print '%20s\t%25s\t%s' % ('', '', ''),
    if i < len(page2): print '\t%20s\t%25s\t%.0f' % (page2[i][0][0:20], page2[i][1][0:25], page2[i][2])
    else: print '\t%20s\t%25s\t%s' % ('', '', '')
    i += 1

print
print 'Avg Price:\t\t\t%f\t%f' % (ct.avg_page_price(page1), ct.avg_page_price(page2))
common, dp = ct.different_prices(page1, page2)
if common != 0: common = float(len(dp))/common*100
if len(dp) == 0: avg = 0
else: avg = tmean(dp)
print '%% Items w/ Diff. Prices:\t%f' % (common)
print 'Price Diff:\t\t\t%f' % (avg)
