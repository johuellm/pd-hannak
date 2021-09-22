#!/usr/bin/env python

import sys, os, time
import hotel_tools as ht

datadir = 'hotels/'

stores = ['expedia'] #'hotels', 

pairs = [('OS', 'control'),('OS', 'win7'),('OS', 'xp'),('OS', 'linux'),('OS', 'osx'),
         ('browser', 'control'),('browser', 'chrome'),('browser', 'ie8'),('browser', 'firefox'),
         ('logged_out', 'control'),('logged_out', 'out'),('logged_out', 'in')]

def make_matrix(starter):
    matrix = {}
    for p1 in pairs:
        matrix[p1] = {}
        for p2 in pairs:
            matrix[p1][p2] = starter
    return matrix

def print_table(results):
    print "& & \\multicolumn{3}{|c|}{Logged In/Out} & \\multicolumn{4}{|c|}{Browser} & \\multicolumn{4}{|c|}{OS} \\\\"
    print "& & In & Out & Con. & FF & IE8 & Chr & Con. & OSX & Lin & XP & Win7 \\\\"
    rows = pairs[:]
    rows.reverse()
    for p1 in pairs:
        rows.pop()
        print "%s & %s" % (p1[0], p1[1]),
        i = 0
        for p2 in rows:
            i += 1
            total, count = results[p1][p2]
            if count: print "& %.2f" % (total/count),
            else: print "& 0.0",
        while i < 11:
            i += 1
            print "&",
        print "\\\\"
    

for hotel in stores:
    jaccard = make_matrix((0.0, 0))
    kt = make_matrix((0.0, 0))
    rows = pairs[:]
    rows.reverse()

    for p1 in pairs:
        rows.pop()

        for folder in os.listdir(os.path.join(datadir, hotel, p1[0])):                    
            timestamp = time.mktime(time.strptime(folder, 'results_%Y_%m_%d_%H'))
            if timestamp > 1397966400 + 60 * 60 * 4: # only consider days before the buckets shuffled
                break
            print 'Running', p1, folder

            for key in ht.keywords:
                try: bpage = ht.parse(hotel, os.path.join(datadir, hotel, p1[0], folder, p1[1], key + '.html'))
                except IOError:
                    #print "Can't find",  os.path.join(datadir, hotel, p1[0], folder, p1[1], key + '.html')
                    continue
                if len(bpage) == 0: continue
        
                for p2 in rows:
                    try: tpage = ht.parse(hotel, os.path.join(datadir, hotel, p2[0], folder, p2[1], key + '.html'))
                    except IOError:
                        #print "Can't find", os.path.join(datadir, hotel, p2[0], folder, p2[1], key + '.html')
                        continue
                    if len(tpage) == 0: continue

                    total, count = jaccard[p1][p2]
                    total += ht.jaccard(bpage, tpage)
                    count += 1
                    jaccard[p1][p2] = (total, count)

                    total, count = kt[p1][p2]
                    edit, k = ht.editdist_and_kendalltau(bpage, tpage)
                    total += k
                    count += 1
                    kt[p1][p2] = (total, count)

    print_table(jaccard)
    print_table(kt)
    

                            

