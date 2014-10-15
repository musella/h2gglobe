#!/bin/env python

from optparse import OptionParser, make_option
import sys, os
import array
from math import sqrt, fabs

def ytitle(h,tit):
    h.GetYaxis().SetTitle( (tit % { "binw" : h.GetBinWidth(0), "xtitle" : h.GetXaxis().GetTitle() }).replace("(GeV)","") )

objs = []

def getCatName(icat, labels=None):
    if labels:
        return labels[icat]
    return "cat%d" % igroup

def setStat(h,prev=None,vert=-1,horiz=0.):
    ROOT.gPad.Update()
    st = h.FindObject('stats')
    st.SetLineColor(h.GetLineColor())
    st.SetTextColor(h.GetLineColor())

    if prev:
        shiftx = (prev.GetX2NDC() - st.GetX1NDC())*horiz
        shifty = (prev.GetY2NDC() - st.GetY1NDC())*vert

        st.SetX1NDC(st.GetX1NDC()+shiftx)
        st.SetX2NDC(st.GetX2NDC()+shiftx)

        st.SetY1NDC(st.GetY1NDC()+shifty)
        st.SetY2NDC(st.GetY2NDC()+shifty)

    ROOT.gPad.Update()
    return st

def trMean(hist,alpha):

    beta = 1.-alpha
    probs = array.array('d',[beta*0.5,1.-beta*0.5])
    quantiles = array.array('d',[0.,0.])

    hist.GetQuantiles(2,quantiles,probs)

    print hist.GetName(), quantiles, probs
    
    limits = [ hist.GetXaxis().FindBin(q) for q in quantiles ]
    hist.GetXaxis().SetRange(*limits)
    
    mean = hist.GetMean()
    err  = hist.GetMeanError() ## hist.GetRMS() / ( ( 1. - beta )*sqrt( hist.Integral() ) )

    if( alpha != 1. ):
        line0 = ROOT.TLine(quantiles[0],hist.GetYaxis().GetXmin(),quantiles[0],hist.GetYaxis().GetXmax())
        line1 = ROOT.TLine(quantiles[1],hist.GetYaxis().GetXmin(),quantiles[1],hist.GetYaxis().GetXmax())
        objs.extend( [line0,line1] )
        line0.SetLineColor(hist.GetLineColor())
        line1.SetLineColor(hist.GetLineColor())
        hist.GetListOfFunctions().Add(line0)
        hist.GetListOfFunctions().Add(line1)
        
    hist.GetXaxis().SetRange()
    return mean,err

def winMean(hist,rng):

    limits = [ hist.GetXaxis().FindBin(q) for q in rng ]
    hist.GetXaxis().SetRange(*limits)
    
    mean = hist.GetMean()
    err  = hist.GetMeanError()
        
    hist.GetXaxis().SetRange()
    return mean,err

def getMean(h,method):
    if type(method) == float:
        print method
        x,xerr = trMean(h,method)
    elif type(method) == tuple:
        x,xerr = winMean(h,method)
    else:
        x,xerr = method(h)

    return 100.*(x-1.),100.*xerr

def recFit(h,start=1.,sigma=1.):
    
    oldmean = start
    oldsigma = sigma
    f = ROOT.TF1("f","gaus",start-sigma,start+sigma)
    ## oldmean = 90.
    ## oldsigma = 10.
    
    h.Fit(f,"LQRN")
    errmean  = f.GetParError(1)
    mean  = f.GetParameter(1)
    sigma = f.GetParameter(2)*1
    iter = 0
    while iter < 5 or ( fabs(oldmean - mean) > 0.005*oldmean and iter < 30 ):
        g = ROOT.TF1("g","gaus",mean-sigma,mean+sigma)
        h.Fit(g,"LQRN")
        oldmean = float(mean)
        oldsigma = float(sigma)
        errmean  = g.GetParError(1)
        mean  = g.GetParameter(1)
        sigma = g.GetParameter(2)*1
        iter+=1
        ## print iter, mean, oldmean, sigma

    fcanv = ROOT.TCanvas("fit_%s" % h.GetName(),"fit_%s" % h.GetName())
    fcanv.cd()
    g = ROOT.TF1("final_fit_%s" % h.GetName(),"gaus",mean-sigma,mean+sigma)
    g.SetLineColor(h.GetLineColor())
    ## h.GetListOfFunctions().Add(g.Clone())
    hp = h.Clone()
    hp.Rebin(10)
    ytitle( hp, "Events / %(binw)s" )
    hp.Fit(g,"LQRO")
    hp.Draw()
    g.Draw("same")
    objs.append(g)
    objs.append(fcanv)
    objs.append(h)
    
    for fmt in ["png"]:
        fcanv.SaveAs( "%s.%s" % ( fcanv.GetName(), fmt ) )
                     
    return mean,errmean
        

def toStr(method):
    if type(method) == float:
        return "%d" % (100.*method)
    elif type(method) == tuple:
        return "%1.2g_%1.2g" % method
    else:
        return method.__name__

def buildCalib(hmcs,name,title,method):
    
    gr = ROOT.TGraphErrors()
    gr.SetName(name)
    gr.SetTitle(title)
    
    for y in sorted(hmcs.keys()):
        x,xerr = getMean(hmcs[y],method)
        ip = gr.GetN()
        gr.SetPoint(ip,x,y)
        gr.SetPointError(ip,xerr,0.)
        
    return gr
    
def main(options,args):

    infile = args[0]
    fin = ROOT.TFile.Open(infile)
    os.chdir(options.outdir)

    ROOT.gStyle.SetOptFit(1)

    results = []
    ## methods = [1,0.95,0.8,0.683,0.5,0.4,0.3,0.2]
    ## methods = [recFit,0.683,(85.,100.),(80.,100.),(86.,96.),(88.,94.)]
    ## methods = [recFit,1.,0.683,(85.,97.),(86.,96.),(88,94),(89,93),(90,92)]
    ## methods = [recFit]
    ## methods = [recFit,1.,0.95,0.8,0.683,0.5]
    methods = [1.,0.95,recFit]
    if len(options.groups) > 0:
        categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
    else:
        categories = [ [i] for i in range(options.ncat) ]
    for igroup,group in enumerate(categories):

        catName = getCatName(igroup,options.labels)
        hdata = fin.Get("th1f_data_mass_cat%d" % group[0]).Clone("data_%s" % catName)

        hmcs = {}
        hmcs[0] = fin.Get("th1f_sig_dymm_mass_m90_cat%d" % group[0]).Clone("mc_%s" % catName)
        
        for isig in range(1,options.nsigma+1):
            hmcs[options.step*float(isig)] = fin.Get("th1f_sig_dymm_mass_m90_cat%d_E_scaleUp0%d_sigma" % (group[0],isig) ).Clone("mc_%s_Up0%d" % (catName,options.step*float(isig)*10.))
            hmcs[-options.step*float(isig)] = fin.Get("th1f_sig_dymm_mass_m90_cat%d_E_scaleDown0%d_sigma" % (group[0],isig) ).Clone("mc_%s_Down0%d" % (catName,options.step*float(isig)*10.))

        for icat in group[1:]:
            hdata.Add( fin.Get("th1f_data_mass_cat%d" % icat) )

            hmcs[0].Add(fin.Get("th1f_sig_dymm_mass_m90_cat%d" % icat))
        
            for isig in range(1,options.nsigma+1):
                hmcs[options.step*float(isig)].Add(fin.Get("th1f_sig_dymm_mass_m90_cat%d_E_scaleUp0%d_sigma" % (icat,isig) ))
                hmcs[-options.step*float(isig)].Add(fin.Get("th1f_sig_dymm_mass_m90_cat%d_E_scaleDown0%d_sigma" % (icat,isig) ))
                

        icat = igroup
        hdata.SetLineColor(ROOT.kBlack)
        hdata.SetMarkerColor(ROOT.kBlack)
        ytitle( hdata, "Events / %(binw)s" )
        for s,h in hmcs.iteritems():
            h.SetLineColor(ROOT.kRed)
            ytitle( h, "Events / %(binw)s" )
        hmcs[0].SetLineColor(ROOT.kBlue)
        
        ## hmcs[0].GetXaxis().SetRangeUser(80.,100.)
        ROOT.gStyle.SetOptFit(1)
        res = {}
        for method in methods:
            name = "mVsDeltaE_%s" % toStr(method)
                
            data = ( getMean(hdata,method), getMean(hmcs[0],method) )
            ### res[method] = ( buildCalib(hmcs,name,";m_{ll#gamma} (GeV/c^{2});#Delta E_{#gamma} / E_{#gamma} (#times 10^{-2})", method ),
            ###                 data )
            ## data = ( (data[0][0]-1., data[0][1]), (data[1][0]-1., data[1][1]) )
            res[method] = ( buildCalib(hmcs,name,";#delta s_{#gamma} (#times 10^{-2});#Delta E_{#gamma} / E_{#gamma} (#times 10^{-2})", method ),
                            data )

        ROOT.gStyle.SetOptFit(0)
        hdata.GetListOfFunctions().Clear()
        for s,h in hmcs.iteritems():
            h.GetListOfFunctions().Clear()

        canv = ROOT.TCanvas(catName, catName )
        canv.cd()

        norm = hdata.GetMaximum() / hmcs[0].GetMaximum() * hmcs[0].Integral()
        hmcs[0].Rebin(4)
        hdata.Rebin(4)
        h = hmcs[0].DrawNormalized("hist",norm)
        ytitle( h, "Events / %(binw)1.1g GeV" )
        st = setStat(h)
        objs.extend((st,h))
        
        hdata.SetLineColor(ROOT.kBlack)
        hdata.SetMarkerColor(ROOT.kBlack)
        hdata.Draw("e sames")
        objs.append(setStat(hdata,st,0.,-1))

        ip = 1
        for s,h in hmcs.iteritems():
            if fabs(s)  != 0.4:
                continue
            h.Rebin(4)
            h.SetLineColor(ROOT.kRed)
            if s < 0:
                h.SetLineStyle(ROOT.kDashed)
            h = h.DrawNormalized("histsames",norm)
            q = setStat(h,st,-1.*ip)
            objs.extend([q,h])
            ip += 1
        objs.append( (canv, hdata, hmcs ))
        
        for fmt in "C","png","pdf":
            canv.SaveAs("%s.%s" % ( canv.GetName(), fmt) )
        
        results.append(res)
        
    objs.append(results)

    meas = {}
    out = open("results.txt","w+")
    out.write(",".rjust(25)+"data,".rjust(13)+"mc,".rjust(13)+"data-mc,".rjust(13)+"err,".rjust(13)+"(data-mc)/err,".rjust(13)+"scale,".rjust(13)+"eScale,".rjust(13)+"eScaleP,".rjust(13)+"eScaleM,".rjust(13)+"\n")
    for method in methods:
        scales = []
        name = "results_%s" % toStr(method)
        canv = ROOT.TCanvas(name,name,2800,2000)
        canv.Divide(options.ncat/2,2)
        objs.append(canv)
        for icat,res in enumerate(results):
            canv.cd(icat+1)
            ROOT.gPad.SetGridx()
            ROOT.gPad.SetGridy()
            calib, data = res[method]
            data,mc = data
            calib.Fit("pol1","QW+")
            func = calib.GetListOfFunctions().At(0)
            scale = func.Eval(data[0])
            err = sqrt(data[1]**2 + mc[1]**2)
            scaleP = func.Eval(data[0]+err)
            scaleM = func.Eval(data[0]-err)
            scales.append( (data[0],mc[0],(data[0]-mc[0]),err,(data[0]-mc[0])/err,scale,0.5*(scaleP-scaleM),scale-scaleM,scaleP-scale) )
            ip = calib.GetN()
            calib.SetPoint( ip, data[0], scale )
            calib.SetPointError( ip, err, 0.5*(scaleP-scaleM) )
            calib.SetMarkerStyle(10)
            calib.Draw("ap")
        for fmt in "C","png","pdf":
            canv.SaveAs("%s.%s" % (canv.GetName(),fmt) )

        out.write( "Method: %s\n" % toStr(method ) )
        for icat, scale in enumerate(scales):
            catName = getCatName(icat,options.labels)
            out.write(("cat: %s ," % catName).ljust(25) )
            for num in scale:
                out.write(("%.4g," % num).rjust(13) )
            out.write("\n")
    out.close()
    out = open("results.txt")
    print out.read()
    
        
if __name__ == "__main__":
    parser = OptionParser(option_list=[
        make_option("-s", "--step",
                    action="store", type="float", dest="step",
                    default=0.2,
                    ),
        make_option("-N", "--nsigma",
                    action="store", type="int", dest="nsigma",
                    default=4,
                    ),
        make_option("-n", "--ncat",
                    action="store", type="int", dest="ncat",
                    default=12,
                    ),
        make_option("-g", "--group", 
                    action="append",  dest="groups",
                    default=[],
                    ),
        make_option("-l", "--label",
                    action="append", dest="labels",
                    default=[],
                    ),
        make_option("-o", "--outdir",
                    action="store", dest="outdir", type="string",
                    default="zmmgScale",
                    ),
        ])
    
    (options, args) = parser.parse_args()
    print options
    if len(options.labels) == 0:
        options.labels = None

    try:
        os.mkdir(options.outdir)
    except:
        pass
    
    sys.argv.append("-b")
    import ROOT
    
    main( options, args )
