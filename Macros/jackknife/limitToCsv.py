#!/usr/bin/env python

from optparse import OptionParser, make_option
import sys

def mkBranch(tree, nt, name, type):
    tree.Branch(name,AddressOf(nt,name),"%s/%s" % (name,type) )

def readBranch(tree, nt, name):
    tree.SetBranchAddress(name,AddressOf(nt,name) )

def getMuByMass(fname, masses=[120.,125.,130.]):
    import ROOT 
    muByMass = {}
    fin = ROOT.TFile.Open(fname)

    nt = ROOT.Entry()
    limit = fin.Get("limit")
    readBranch(limit,nt,"limit")
    readBranch(limit,nt,"mh")
    readBranch(limit,nt,"quantileExpected")

    for ie in range(limit.GetEntries()):
        limit.GetEntry(ie)
        if nt.quantileExpected == -1 and nt.mh in masses:
            muByMass[nt.mh] = nt.limit
    
    return muByMass


def main(options,args):
    import ROOT

    ROOT.gROOT.ProcessLine( \
       "struct Entry{          \
           double limit;       \
           double mh;          \
           float quantileExpected; \
          };"
       )

    target = args.pop(0)
    labels = [ l for l in options.labels.split(",") if l !="" ]
    masses = [ float(m) for m in options.masses.split(",") if m !="" ]

    if options.npart == 0:
        log = open("%s/%s/split.log" % ( target, labels[0] ), "r" )
        options.npart = int(log.readlines()[-1].split(" ")[-1])
        log.close()
        
    out = open("%s/scan.csv" % target,"w+")
    results = []
    for ipart in range(options.npart):
        results.append({})
        for l in labels:
            fname = "%s/%s/part%d/%s" % ( target, l, ipart, options.resultsName )
            try:
                results[-1][l] = getMuByMass(fname,masses)
            except:
                print fname, l

        line = "%d," % ipart
        skip = False
        for m in masses:
            line += "%1.1f," % m
            for l in labels:
                try:
                    line += "%f," % results[-1][l][m]
                except:
                    print "missing %d %s %f" % ( ipart, l, m )
                    skip = True
        if not skip:
            out.write("%s\n" % line)
        
    
    
if __name__ == "__main__":
    parser = OptionParser(option_list=[
        make_option("-n", "--npart",
                    action="store", dest="npart", type="int",
                    default=0,
                    help="default: %default", metavar=""
                    ),
        make_option("-l", "--labels",
                    action="store", dest="labels", type="string",
                    default="CiC,massfac",
                    help="default: %default", metavar=""
                    ),
        make_option("-m", "--masses",
                    action="store", dest="masses", type="string",
                    default="120,125,130",
                    help="default: %default", metavar=""
                    ),
        make_option("-r", "--resultsName",
                    action="store", dest="resultsName", type="string",
                    default="BestMu/higgsCombineBestMu.MaxLikelihoodFit_blind.root",
                    help="default: %default", metavar=""
                    ),
        ]
                          )

    (options, args) = parser.parse_args()

    print options, args

    sys.argv.append("-b")
    from ROOT import AddressOf
    
    main( options, args ) 

