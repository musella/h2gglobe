#!/bin/env python

import sys, types, os
import commands
import numpy
from math import sqrt, log, fabs
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '1.3g')

from optparse import OptionParser, make_option
from  pprint import pprint
from copy import deepcopy as copy

objs = []

class MyAppend:
    def __init__(self):
        self.cold = True
        
    def __call__(self,option, opt_str, value, parser, *args, **kwargs):
        target = getattr(parser.values,option.dest)
        if self.cold:
            del target[:]
        self.cold = False
        target.append(value)
                                                    
def setAliases(tree,variations):
    tot= ""
    for name, defs in variations.iteritems():
        cat, unc = defs
        tree.SetAlias("deltaE%s" % name, "(%s)*%1.2g" % (cat,unc) )
        
        if tot != "":
            tot += "+"
        tot += "deltaE%s" % name
    tree.SetAlias("deltaE",tot)
    
    
def readcats(fname):
    fin = open(fname)
    variations = {}
    for line in fin.read().split("\n"):
        if line.startswith("#"): continue
        toks = [ t for t in line.replace("\t"," ").split(" ") if t != "" ]
        if len(toks) > 0:
            name   = toks.pop(0)
            toks.pop(0)
            mineta = float(toks.pop(0))
            maxeta = float(toks.pop(0))
            minr9  = float(toks.pop(0))
            maxr9  = float(toks.pop(0))
            toks.pop(0)
            toks.pop(0)
            toks.pop(0)
            unc    = float(toks.pop(0))

            cat = "(abs(sceta) >= %1.3g && abs(sceta) < %1.3g && r9 >= %1.3g && r9 < %1.3g)" % ( mineta, maxeta, minr9, maxr9  )
            variations[name] = ( cat, unc )
            
    return variations

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    all = []
    allnuis = []
    for inf,nuis in zip(options.infile,options.nuisances):
        variations = readcats(inf)
        nuisances  = readcats(nuis)
        all.append( (variations,nuisances) )

    procs = ["dymm_m90"]
    procvars = {}
    first = True
    for fname in args:
        tin = ROOT.TFile.Open(fname)
            
        for proc in procs:
            tree = tin.Get("zmmgAnalysis/%s" % ( proc ) )
            objs.append(tree)

            for variations,nuisances in all:
                aliases = setAliases(tree,variations)
                
                for name,defs in nuisances.iteritems():
                    allnuis.append(name)
                    cat, dum = defs
                    tree.Draw("deltaE*(%s):category>>hshift(24,-0.5,23.5,1001.,-1.0001e-2,1.0001e-2)" % (cat),"weight","goff")
                    h = ROOT.gDirectory.Get("hshift")
                    prf = h.ProfileX("%s_%s" % ( proc, name ) )
                    objs.append(prf)
                    h.Delete()                    
                    procvars["%s_%s" % ( proc, name )] = prf
            first = False
            

    print "cat,",
    for name in allnuis:
        print "%s," % name,
    print "tot"
    for cat in range(24):
        print "%d," % cat,
        for proc in procs:
            tot = 0.
            for variations,nuisances in all:
                for name,defs in nuisances.iteritems():
                    prf = procvars["%s_%s" % ( proc, name )]
                    var = fabs(prf.GetBinContent(cat+1))
                    ## print name, ",%1.3g,%1.3g" % ( var, prf.GetBinError(cat+1) )
                    print "%1.3g," % ( var ),
                    tot += var*var
            print "%1.3g" % sqrt(tot)

    
if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-i", "--infile",
                        action="append", type="string", dest="infile",
                        default=[],
                        help="input file",
                        ),
            make_option("-n", "--nuisances",
                        action="append", type="string", dest="nuisances",
                        default=[],
                        help="input file",
                        ),
            make_option("-s", "--sqrts",
                        action="store", type="string", dest="sqrts",
                        default="8TeV",
                        help="",
                        ),
            make_option("-o", "--outfile",
                        action="store", type="string", dest="outfile",
                        default="nuisvar.json",
                        help="output file",
                        )
            ])
    
    (options, args) = parser.parse_args()
    
    ## print "\n---------------------------------------------"
    ## print "Job options "
    ## pprint(options.__dict__)
    
    import ROOT
    ## print ROOT.gROOT.IsBatch()
    

    ws=main(options,args)
