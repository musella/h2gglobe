#!/bin/env python

import sys
from optparse import OptionParser

usage = "usage: %prog [options] fileName"
parser = OptionParser(usage=usage)
parser.add_option('-o','--output',dest='output',type='string',default='stdout',help=' output file')
(options,args)=parser.parse_args()

if len(args) <= 0:
        parser.error("incorrect number of arguments")
outputfile=options.output
if 'stdout' in outputfile:
	outputfile="/dev/stdout"
out=open(outputfile,"w")	

#iname=sys.argv[1]
iname=args[0]

r9map = { "gold" : ("Gold",(0.94,999)),
          "bad"  : ("Bad",(-999,0.94)),
          }
etamap = { "0_1"   : "LowEta",
           "1_1.5" : "HighEta",
           "1.5_2" : "LowEta",
           "2_3"   : "HighEta",
    }

input=open(iname,'r')
lastcat = None
infoline=False
for line in input.read().split("\n"):
    toks = [ l for l in line.split("\t") if l != "" ]
    if len(toks) == 6:
        cat,first,last,corr,err = toks[0], int(toks[2]), int(toks[3]), float(toks[4]), float(toks[5])
        corr = 1. - corr
        det,eta, r9 = cat.split('-') 
        etaRng = eta.split("_")[1:3]
        if etaRng[1] == '2.5':
            etaRng[1] = '3'
        elif etaRng[1] == '1.4442':
            etaRng[1] = '1.5'
        elif etaRng[0] == '1.566':
            etaRng[0] = '1.5'
        
        r9Lab, r9Rng = r9map[r9]
        typ = 0
        etaLab = etamap[ "%s_%s" % ( etaRng[0], etaRng[1] ) ]
        cat = "%s%s%s" % ( det, etaLab, r9Lab )
        if cat != lastcat:
            print >>out
        lastcat = str(cat)
	if not infoline:
		print >>out, "#cat typ eta0 eta1 r9 r9 first last corr err"
		infoline=True
        print >>out, "%s %d %s %s %1.2f %1.2f %d %d %1.3g %1.3g" % (cat,  typ, etaRng[0], etaRng[1], r9Rng[0], r9Rng[1], first, last,  corr, err )
        ## print det, etaRng, r9Lab, r9Rng, first,last,corr,err
    elif len(toks) == 11:
        cat,et0,et1,first,last,corr,err = toks[0], int(toks[2]), int(toks[3]), int(toks[4]),int(toks[5]),float(toks[9]), float(toks[10])
        corr = 1. - corr
        eta, r9 = cat.split('-')
	det='EB'
        etaRng = eta.split("_")[1:3]
        if etaRng[1] == '2.5':
            etaRng[1] = '3'
        elif etaRng[1] == '1.4442':
            etaRng[1] = '1.5'
        elif etaRng[0] == '1.566':
            etaRng[0] = '1.5'
        
        r9Lab, r9Rng = r9map[r9]
        typ = 0
	pivot = 0 
	stoc = 0 
	stocerr = 0
        etaLab = etamap[ "%s_%s" % ( etaRng[0], etaRng[1] ) ]
        cat = "%s%s%s" % ( det, etaLab, r9Lab )
        if cat != lastcat:
            print >>out
	if not infoline:
		print >>out, "#cat typ et0 et1 eta0 eta1 r9 r9 first last pivot offset err stoc err"
		infoline=True
        print >>out,"%s %d %d %d %s %s %1.2f %1.2f %d %d %1.3g %1.3g" % (cat,  typ, et0, et1 ,etaRng[0], etaRng[1], r9Rng[0], r9Rng[1], first, last, pivot, corr, err, stoc ,stocerr )
        print >>out,"%s %d %d %d %s %s %1.2f %1.2f %d %d %1.3g %1.3g" % (cat,  typ, et0, et1 ,-etaRng[0], -etaRng[1], r9Rng[0], r9Rng[1], first, last,  pivot, corr, err, stoc, stocerr )
	
    else:
	if len(toks)>0:
		print >>sys.stderr, "Error on line (don't know what to do):\n %s"%line

        

