#!/usr/bin/env python

from optparse import OptionParser, make_option
import sys, os

def mkBranch(tree, nt, name, type):
    tree.Branch(name,AddressOf(nt,name),"%s/%s" % (name,type) )

def readBranch(tree, nt, name):
    tree.SetBranchAddress(name,AddressOf(nt,name) )

def main(options,args):
    import ROOT

    ROOT.gROOT.ProcessLine( \
       "struct Entry{          \
           double limit;       \
           double mh;          \
           double quantileExpected; \
          };"
       )

    nt = ROOT.Entry()

    if "CiC" in os.path.dirname(os.path.dirname(os.path.dirname(args[0]))):
        options.seed += 417983
    print options
    ROOT.gRandom.SetSeed(options.seed)
    shift = ROOT.gRandom.Uniform(options.range)

    fin = ROOT.TFile.Open(args.pop(0))
    fout = ROOT.TFile.Open(args.pop(0),"recreate")

    limit = fin.Get("limit")
    fout.cd()
    blind = ROOT.TTree("limit","limit")

    readBranch(limit,nt,"limit")
    readBranch(limit,nt,"mh")
    readBranch(limit,nt,"quantileExpected")

    mkBranch(blind,nt,"limit","D")
    mkBranch(blind,nt,"mh","D")
    mkBranch(blind,nt,"quantileExpected","F")
    
    for ie in range(limit.GetEntries()):
        limit.GetEntry(ie)
        nt.limit += shift
        blind.Fill()

    blind.Write()
    rndSeed = ROOT.TParameter("int")("seed",options.seed)
    rndRange = ROOT.TParameter("float")("range",options.range)

    rndSeed.Write()
    rndRange.Write()

    fout.Close()
    fin.Close()
    
if __name__ == "__main__":
    parser = OptionParser(option_list=[
        make_option("-s", "--seed",
                    action="store", dest="seed", type="int",
                    default=8964231,
                    help="default: %default", metavar=""
                    ),
        make_option("-r", "--range",
                    action="store", dest="range", type="float",
                    default=5.,
                    help="default: %default", metavar=""
                    ),
        ]
                          )

    (options, args) = parser.parse_args()

    print options, args

    sys.argv.append("-b")
    from ROOT import AddressOf
    
    main( options, args ) 

