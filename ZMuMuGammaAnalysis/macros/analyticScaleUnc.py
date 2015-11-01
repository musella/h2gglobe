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
            
            ## cat = "(abs(sceta) > %1.3g && abs(sceta) <= %1.3g && r9 > %1.3g && r9 <= %1.3g)" % ( mineta, maxeta, minr9, maxr9  )
            cat = "(abs(photon.Eta()) > %1.3g && abs(photon.Eta()) <= %1.3g && cat_r9 > %1.3g && cat_r9 <= %1.3g)" % ( mineta, maxeta, minr9, maxr9  ) ## bug in tree filling so r9 and sceta are not reliable
            variations[name] = ( cat, unc )
            
    return variations


def getCatName(icat, labels=None):
    if labels:
        return labels[icat]
    return "cat%d" % icat

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    allvars = []
    allnuis = []
    for inf,nuis in zip(options.infile,options.nuisances):
        variations = readcats(inf)
        nuisances  = readcats(nuis)
        allvars.append( (variations,nuisances) )

    if len(options.groups) > 0:
        categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
    else:
        categories = [ [i] for i in range(options.ncat) ]
    if len(options.labels) <= 0:
        options.labels = None

    procs = ["dymm_m90"]
    procvars = {}
    first = True
    for fname in args:
        tin = ROOT.TFile.Open(fname)
            
        for proc in procs:
            tree = tin.Get("zmmgAnalysis/%s" % ( proc ) )
            objs.append(tree)
            
            tree.SetAlias("cat_r9","0.*(category%2==1) + 0.95*(category%2==0)") ## bug in tree filling so r9 is not reliable
            
            for variations,nuisances in allvars:
                aliases = setAliases(tree,variations)
                
                for name,defs in nuisances.iteritems():
                    allnuis.append(name)
                    cat, dum = defs
                    draw = "deltaE*(%s):category>>hshift(%d,-0.5,%f,1001.,-1.0001e-2,1.0001e-2)" % (cat,options.ncat,float(options.ncat)-0.5)
                    print draw
                    tree.Draw("deltaE*(%s):category>>hshift(%d,-0.5,%f,1001.,-1.0001e-2,1.0001e-2)" % (cat,options.ncat,float(options.ncat)-0.5),
                              "weight","goff")
                    h = ROOT.gDirectory.Get("hshift")
                    prf = h.ProfileX("%s_%s" % ( proc, name ) )
                    objs.append(prf)
                    h.Delete()                    
                    procvars["%s_%s" % ( proc, name )] = prf
            
            if first:
                tree.Draw("category>>hweight_%s(%d,-0.5,%f)" % (proc,options.ncat,float(options.ncat)-0.5),"weight","goff")
                procvars["%s" % ( proc )] = ROOT.gDirectory.Get("hweight_%s"%proc)
        first = False
        

    print "cat,",
    for name in allnuis:
        print "%s," % name,
    print "tot, tot_weight"
    #### for cat in range(24):
    ####     print "%d," % cat,
    ####     for proc in procs:
    ####         tot = 0.
    ####         for variations,nuisances in allvars:
    ####             for name,defs in nuisances.iteritems():
    ####                 prf = procvars["%s_%s" % ( proc, name )]
    ####                 var = prf.GetBinContent(cat+1)*options.rescale
    ####                 ## print name, ",%1.3g,%1.3g" % ( var, prf.GetBinError(cat+1) )
    ####                 print "%1.3g," % ( var ),
    ####                 tot += var*var
    ####         print "%1.3g," % sqrt(tot),
    ####         print "%1.3g"  % procvars["%s"%proc].GetBinContent(cat+1)

    for igroup,group in enumerate(categories):
        name = getCatName(igroup,options.labels)
        ## print "%d," % igroup,
        print "%s," % name, 
        gvars = { nuis : 0. for nuis in allnuis }
        gvars["tot"] = 0.
        gvars["tot_weight"] = 0.
        for cat in group:
            for proc in procs:
                tot = 0.
                weight = procvars["%s"%proc].GetBinContent(cat+1)
                gvars["tot_weight"] += weight
                for variations,nuisances in allvars:
                    for name,defs in nuisances.iteritems():
                        prf = procvars["%s_%s" % ( proc, name )]
                        var = prf.GetBinContent(cat+1)*options.rescale
                        gvars[name]   += var*weight
        for name in allnuis:
            print "%1.3g," % ( gvars[name]/gvars["tot_weight"] ),
            gvars["tot"] += (gvars[name]*gvars[name])/(gvars["tot_weight"]*gvars["tot_weight"])
        print "%1.3g," % sqrt(gvars["tot"]),
        print "%1.3g" % gvars["tot_weight"]
        
    
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
            make_option("-r", "--rescale",
                        action="store", type="float", dest="rescale",
                        default=1.,
                        help="",
                        ),
            make_option("-o", "--outfile",
                        action="store", type="string", dest="outfile",
                        default="nuisvar.json",
                        help="output file",
                        ),
            make_option("-g", "--group", 
                        action="append",  dest="groups",
                        default=[],
                        ),
            make_option("-l", "--label", 
                        action="append",  dest="labels",
                        default=[],
                        ),
            make_option("--ncat",
                        action="store", type="int", dest="ncat",
                        default=24,
                        ),

            ])
    
    (options, args) = parser.parse_args()
    
    ## print "\n---------------------------------------------"
    ## print "Job options "
    ## pprint(options.__dict__)
    
    import ROOT
    ## print ROOT.gROOT.IsBatch()
    

    ws=main(options,args)
