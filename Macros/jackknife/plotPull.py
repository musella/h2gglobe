#!/usr/bin/env python

from optparse import OptionParser, make_option
import sys
import json 
from pprint import pprint 
from math import fabs
import operator
import random
import ROOT
from copy import copy

isMVA=False
objs = []

import math

Sqrt = math.sqrt
Power = math.pow

def nu(sa,sb,r,mua,mub):
    Delta = Sqrt(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4))

    dena = (Sqrt(2)*Sqrt(Delta + Power(sa,2) - Power(sb,2))*Power(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4),0.25))
    aa = -2*r*sa*sb
    ab = (Delta + Power(sa,2) - Power(sb,2))
    nua = ( aa*mua + mub*ab) / dena

    denb = (Sqrt(2)*Sqrt(Delta - Power(sa,2) + Power(sb,2))*Power(Power(sa,4) + 2*(-1 +2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4),0.25))
    ba = 2*r*sa*sb
    bb = (Delta - Power(sa,2) + Power(sb,2))
    nub = ( ba*mua + mub*bb )/denb

    print aa/dena, ab/dena
    print ba/denb, bb/denb
   
    return nua, nub

def sig(sa,sb,r,mua,mub,sai,sbi):
    Delta = Sqrt(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4))

    dena = (Sqrt(2)*Sqrt(Delta + Power(sa,2) - Power(sb,2))*Power(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4),0.25))
    aa = -2*r*sa*sb
    ab = (Delta + Power(sa,2) - Power(sb,2))
    
    denb = (Sqrt(2)*Sqrt(Delta - Power(sa,2) + Power(sb,2))*Power(Power(sa,4) + 2*(-1 +2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4),0.25))
    ba = 2*r*sa*sb
    bb = (Delta - Power(sa,2) + Power(sb,2))

    siga = Sqrt(sai*sai*aa*aa + sbi*sbi*ab*ab + 2.*sai*sbi*r*aa*ab)/dena 
    sigb = Sqrt(sai*sai*ba*ba + sbi*sbi*bb*bb + 2.*sai*sbi*r*ba*bb)/denb 
    
    ## siga = (Power(sai,2)*(Delta + Power(sb,2)) - 4*Power(r,2)*sa*sai*sb*sbi + (Delta - Power(sb,2))*Power(sbi,2) + Power(sa,2)*(-Power(sai,2) + Power(sbi,2)))/(2.*Sqrt(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4)))

    ## sigb = (Power(sai,2)*(Delta - Power(sb,2)) + 4*Power(r,2)*sa*sai*sb*sbi + (Delta + Power(sb,2))*Power(sbi,2) + Power(sa,2)*(sai - sbi)*(sai + sbi))/(2.*Sqrt(Power(sa,4) + 2*(-1 + 2*Power(r,2))*Power(sa,2)*Power(sb,2) + Power(sb,4)));

    return siga, sigb

def main(options,args):

    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetOptStat(111111)
    ROOT.gStyle.SetOptFit(1)
    
    pulls = []
    dpulls = []
    
    muMVA = (0.54,0.31,0.26)
    muCiC = (0.96,0.37,0.33)
    corr = 0.76
    
    pullCiCOnMVA = (0.54,0.50,0.11)
    pullCiCOnOverlap = (0.75,0.75,0.13)
    pullCiCvsSumpt2 = (1.19,0.96,0.14)
    
    muMVANvtx = [(0.79,0.44,0.42),(0.71,0.56,0.49),(0.02,0.49,0.47)]
    muCiCNvtx = [(1.36,0.53,0.59),(1.05,0.61,0.69),(0.51,0.61,0.63)]

    pulls.append( pullCiCvsSumpt2 )
    pulls.append( pullCiCOnMVA )
    pulls.append( pullCiCOnOverlap )

    sMVA = Sqrt(muMVA[1]*muMVA[2])
    sCiC = Sqrt(muCiC[1]*muCiC[2])
    nuA, nuB = nu(sMVA, sCiC, corr, muMVA[0], muCiC[0])
    sA, sB = sig(sMVA, sCiC, corr, muMVA[0], muCiC[0], sMVA, sCiC)
    print "input", muMVA[0], muCiC[0]
    print "A", nuA, sA
    print "B", nuB, sB
    ## for mva,cic in zip(muCiCNvtx,muCiCNvtx):
    for i in range(len(muMVANvtx)):
        mva = muMVANvtx[i]
        cic = muCiCNvtx[i]
        mua = mva[0]
        sai = Sqrt(mva[1]*mva[2])
        mub = cic[0]
        sbi = Sqrt(cic[1]*cic[2])
        nua, nub = nu(sMVA, sCiC, corr, mua, mub)
        siga, sigb = sig(sMVA, sCiC, corr, mua, mub, sai, sbi)
        
        ## siga *= Sqrt(2./3.)
        ## sigb *= Sqrt(2./3.)
        ## siga *= 2./3.
        ## sigb *= 2./3.
        ## siga *= Sqrt( sMVA*sMVA - siga*siga ) / sMVA
        ## siga *=  Sqrt(siga**2 - sA**2 ) / siga
        ## sigb *=  Sqrt(sigb**2 - sB**2 ) / sigb
        
        pulls.append( (nua, nuA, siga, ) )
        pulls.append( (nub, nuB, sigb, ) )

        print "input", mua, mub
        print "A", nua, siga
        print "B", nub, sigb
        
    chi2 = 0.
    tpull = ROOT.TNtuple("tpull","tpull","pull")
    hpull = ROOT.TH1F("pull","pull",5,-3,3)
    gpull = ROOT.TGraphErrors()
    ## hpull = ROOT.TH1F("pull","pull",11,-3.15,3.15)
    ## hpull = ROOT.TH1F("pull","pull",11,-2.625,2.625)
    ## hpull = ROOT.TH1F("pull","pull",5,-2.5,2.5)
    for val,nom,err in pulls:
        pull = (val-nom)/err
        print pull,val,nom,err
        hpull.Fill( (val-nom)/err )
        tpull.Fill( pull )
        chi2 += pull*pull
        ipoint = gpull.GetN()
        gpull.SetPoint( ipoint, abs(val-nom)/err, ipoint+1 )
        gpull.SetPointError( ipoint, 1., 0. )
        
    ## hdpull = ROOT.TH1F("dpull","dpull",11,-2.625,2.625)
    hdpull = ROOT.TH1F("dpull","dpull",5,-3.,3)
    for val,nom,err in dpulls:
        pull = (val-nom)/err
        ## print pull,val,nom,err
        hdpull.Fill( (val-nom)/err )
    hdpull.SetFillColor(ROOT.kRed)

    ndf = len(pulls) - 2
    prb = ROOT.TMath.Prob(chi2,ndf)
    sf = ROOT.RooStats.PValueToSignificance(1.-prb)
    print chi2, ndf, prb, sf
    
    w = ROOT.RooWorkspace("w",True)
    gaus = w.factory("Gaussian::gauss(pull[0,-10.,10.],mean[0,-10.,10.],sigma[1.,0.,10.])");
    vpull = w.var("pull")
    mean = w.var("mean")
    mean.setConstant()
    sigma = w.var("sigma")
    ds = ROOT.RooDataSet("dpull","dpull",tpull,ROOT.RooArgSet(vpull))
    getattr(w,"import")(ds)
    gaus.fitTo(ds)
    ### f = ROOT.TF1("ugaus","gaus",-10,10)
    ### hpull.Fit("ugaus")
    ### f.FixParameter(0)
    ### tpull.UnbinnedFit("ugaus","pull")
    ### hpull.Draw("")
    ## f.Draw("same")
    ## hdpull.Draw("hist same")

    frame = vpull.frame(ROOT.RooFit.Range(-3,3),ROOT.RooFit.Bins(5))
    ## ds.plotOn(frame,ROOT.RooFit.DrawOption("B"),ROOT.RooFit.FillStyle(0),ROOT.RooFit.DataError(ROOT.RooAbsData.None),ROOT.RooFit.XErrorSize(0))
    ## ds.plotOn(frame,ROOT.RooFit.Invisible())
    ds.plotOn(frame)
    gaus.plotOn(frame)
    gaus.paramOn(frame)
    ## frame.Draw()
    ## hpull.Draw("same")
    ## frame.Draw("same")

    gpull.Print()
    gpull.GetXaxis().SetTitle("| #delta #mu / #sigma |")
    gpull.GetYaxis().SetTitle("")
    
    gpull.SetMarkerStyle(ROOT.kFullSquare)
    gpull.Draw("APE")
    zero = ROOT.TLine(0.,0.,0.,len(pulls)+0.8)
    zero.Draw("same")
    text = ROOT.TLatex()
    text.DrawLatex(-1,len(pulls)+1.1,"#chi_{obs}^{2} / n.d.f = %1.1f / %1.0f" % (chi2,ndf))
    text.DrawLatex(1,len(pulls)+1.1,"p( #chi^{2} > #chi_{obs}^{2} | n.d.f ) = %1.1f" % (prb))
    
    objs.append( ( hpull, hdpull, gpull, zero ) )
    
if __name__ == "__main__":
    parser = OptionParser(option_list=[
        make_option("--randomSeed",
                    action="store", type="int", dest="randomSeed",
                    default=None,
                    help="default : %default", metavar=""
                    ),
        
        ])
    
    (options, args) = parser.parse_args()

    print options, args

    ## sys.argv.append("-b")
    main( options, args ) 
