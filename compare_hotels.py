#!/usr/bin/env python

import sys
from scipy.stats import tmean
import hotel_tools as ht

if len(sys.argv) < 3:
    print 'Usage: # [-a]', sys.argv[0], '<hotel> <page 1> <page 2>'
    sys.exit()

if sys.argv[1] == '-a':
    page1 = ht.parse_ads(sys.argv[2], sys.argv[3])
    page2 = ht.parse_ads(sys.argv[2], sys.argv[4])
else:
    page1 = ht.parse(sys.argv[1], sys.argv[2])
    page2 = ht.parse(sys.argv[1], sys.argv[3])    

common, dp, disc = ht.different_prices(page1, page2, True)

l = max(len(page1), len(page2))
i = 0
while i < l:
    if i < len(page1):
        if page1[i][0] not in disc: print '%25s   %.2f' % (page1[i][0][0:25], page1[i][1]),
        else: print '%25s * %.2f' % (page1[i][0][0:25], page1[i][1]),
    else: print '%25s   %s' % ('', '  '),
    if i < len(page2):
        if page2[i][0] not in disc: print '\t%25s   %.2f' % (page2[i][0][0:25], page2[i][1])
        else: print '\t%25s * %.2f' % (page2[i][0][0:25], page2[i][1])
    else: print '\t%25s   %s' % ('', '  ')
    i += 1

print
j, intersect, length = ht.jaccard(page1, page2, True)
print 'Page length:\t\t\t%i\t\t%i' % (len(page1), len(page2))
print 'Jaccard:\t\t\t%f\t(%i out of %i)' % (j, intersect, length)
ed, kt = ht.editdist_and_kendalltau(page1, page2)
print 'Edit Dist:\t\t\t%f' % (ed)
print 'Kendall Tau:\t\t\t%f' % (kt)
n = ht.ndcg([page1, page2])
print 'NDCG:\t\t\t\t%f\t%f' % (n[0], n[1])
print 'Avg Price:\t\t\t%f\t%f' % (ht.avg_page_price(page1), ht.avg_page_price(page2))
if common != 0: common = float(len(dp))/common*100
if len(dp) == 0: avg = 0
else: avg = tmean(dp)
print '%% Items w/ Diff. Prices:\t%f' % (common)
print 'Price Diff:\t\t\t%f' % (avg)
