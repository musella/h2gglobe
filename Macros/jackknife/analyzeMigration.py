#!/usr/bin/env python

from optparse import OptionParser, make_option
import sys

def main(options,args):
    import ROOT

    input = args.pop(0)
    output = input.replace(".root","_analysis")
    fin = ROOT.TFile.Open(input)

    xtit,ytit = options.labels.split(",")

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat("1.0f")
    ROOT.gStyle.SetLabelSize(0.1,"XYZ")

    migration = fin.Get("migration")
    migration.GetXaxis().SetTitle(xtit)
    migration.GetYaxis().SetTitle(ytit)
    migration.GetXaxis().SetBinLabel(1,"not sel.")
    migration.GetYaxis().SetBinLabel(1,"not sel.")
    for ibin in range(2,migration.GetNbinsX()+1):
        migration.GetXaxis().SetBinLabel(ibin,"cat%d" % (ibin - 2))
    for ibin in range(2,migration.GetNbinsY()+1):
        migration.GetYaxis().SetBinLabel(ibin,"cat%d" % (ibin - 2))
    
    normByRow = migration.Clone("normByRow")
    normByRow.SetTitle("normByRow")
    normByRow.GetZaxis().SetTitle("%")
    normByCol = normByRow.Clone("normByCol")
    normByCol.SetTitle("normByCol")

    normByOverlap = normByRow.Clone("normByOverlap")
    normByOverlap.SetTitle("normByOverlap")
    
    total    = migration.Integral()
    common   = migration.Integral(2,-1,2,-1)
    firstRow = migration.Integral(-1,-1,1,1)
    firstCol = migration.Integral(1,1,-1,-1)

    

    print "total:    ", total
    print "common:   ", common, common / total * 100.
    print normByCol.GetXaxis().GetTitle(),": ", firstRow, firstRow / total * 100.
    print normByRow.GetYaxis().GetTitle(),": ", firstCol, firstCol / total * 100.
    print 
    
    print normByCol.GetXaxis().GetTitle()
    for ibin in range(1,normByCol.GetNbinsX()+1):
        totCol = normByCol.Integral(ibin,ibin,-1,-1)
        print ibin -2, totCol
        if totCol == 0:
            continue
        for jbin in range(1,normByCol.GetNbinsY()+1):
            bin = normByCol.GetBinContent(ibin,jbin)
            if bin == 0:
                continue
            normByCol.SetBinContent(ibin,jbin,bin/totCol * 100.)
    print
            
    print normByRow.GetYaxis().GetTitle()
    for jbin in range(1,normByRow.GetNbinsY()+1):
        totRow = normByRow.Integral(-1,-1,jbin,jbin)
        print jbin -2, totRow
        if totRow == 0.:
            continue
        for ibin in range(1,normByRow.GetNbinsX()+1):
            bin = normByRow.GetBinContent(ibin,jbin)
            if bin == 0:
                continue
            normByRow.SetBinContent(ibin,jbin,bin/totRow * 100.)
    print
    
    for ibin in range(1,normByCol.GetNbinsX()+1):
        totCol = migration.Integral(ibin,ibin,-1,-1)
        for jbin in range(1,migration.GetNbinsY()+1):
            totRow = migration.Integral(-1,-1,jbin,jbin)
            bin = migration.GetBinContent(ibin,jbin)
            if bin == 0:
                continue
            normByOverlap.SetBinContent(ibin,jbin,bin/(totCol+totRow-bin) * 100.)

    migration.SetMarkerSize(2.2)
    normByRow.SetMarkerSize(4)
    normByRow.GetZaxis().SetRangeUser(0.,100.)
    normByCol.SetMarkerSize(4)
    normByCol.GetZaxis().SetRangeUser(0.,100.)
    normByOverlap.SetMarkerSize(4)
    normByOverlap.GetZaxis().SetRangeUser(0.,50.)
    c = ROOT.TCanvas("migration_analysis","migration_analysis",1600,800)
    ### global c, normByRow, normByCol, normByOverlap
    c.Divide(2,2)
    c.cd(1)
    migration.Draw("colz text")
    c.cd(2)
    normByOverlap.Draw("colz text")
    c.cd(3)
    normByCol.Draw("colz text")
    c.cd(4)
    normByRow.Draw("colz text")

    
    for fmt in "C", "png", "pdf":
        c.SaveAs("%s.%s" % ( output, fmt ))
    
if __name__ == "__main__":
    parser = OptionParser(option_list=[
        make_option("-l", "--labels",
                    action="store", dest="labels", type="string",
                    default="CiC,massfac",
                    help="default: %default", metavar=""
                    ),
        ]
                          )

    (options, args) = parser.parse_args()

    ### print options, args

    sys.argv.append("-b")
    from ROOT import AddressOf
    
    main( options, args ) 

