#!/bin/env python

from pyrapp import *
from optparse import OptionParser, make_option

from copy import copy
from pprint import pprint
import csv,os

from math import sqrt

import array

# ------------------------------------------------------------------------------------------
class ZmmgBins(PlotApp):

    def __init__(self):
        super(ZmmgBins,self).__init__(option_list=[
            make_option("--etabins",dest="etabins",action="callback",callback=optpars_utils.ScratchAppend(),
                        default=[0.0,0.9,1.5,2.5]),
            make_option("--ptbins",dest="ptbins",action="callback",callback=optpars_utils.ScratchAppend(),
                        default=[20.,25.,30.,40.,60.]),
            make_option("--r9bins",dest="r9bins",action="callback",callback=optpars_utils.ScratchAppend(),
                        default=[0.,0.94,1]),
            make_option("-n", "--ncat",
                        action="store", type="int", dest="ncat",
                        default=12,
                        ),
            make_option("-g", "--group", 
                        action="append",  dest="groups",
                        default=[],
                        ),
            make_option("--label",
                        action="append", dest="labels",
                        default=[],
                        ),
            make_option("--scanSign",dest="scanSign",action="store",type="float",
                        default=1.),
            make_option("--doScan",dest="doScan",action="callback",callback=optpars_utils.Load(),type="string",
                        default={}),
            make_option("--scanVar",dest="scanVar",action="store",type="string",
                        default="#deltaE_{#gamma}"),
            ]
                                      )
        
        global ROOT, style_utils
        import ROOT
        import pyrapp.style_utils as style_utils
        

    def __call__(self,options,args):
        
        self.loadRootStyle()

        ## ROOT.TGaxis.SetMaxDigits(3)
        ROOT.gStyle.SetTitleYOffset(1.58)

        if options.doScan:
            self.doScan(options,args)
        else:
            self.doBins(options,args)
        
    def doScan(self,options,args):
        
        ### fileName = options.doScan
        ### scan = json.loads( open(fileName).read() )
        ### 
        ### varName = os.path.basename( fileName ).replace("scan_","").replace(".json","")
        varName = options.scanVar
        fileName = varName.replace(" ","").replace("#","").replace("{","").replace("}","").replace("_","").replace("^","").replace("/","")
        
        self.setStyle("TLine",[["SetLineWidth",2]])
        
        scan = options.doScan
        
        gr = ROOT.TGraph()
        for point,val in scan.iteritems():
            nll,stat = val
            if stat != 0: continue
            gr.SetPoint( gr.GetN(), options.scanSign*float(point), nll )
            

        gr.Fit("pol2")
        b = gr.GetListOfFunctions().At(0).GetParameter(1)
        a = gr.GetListOfFunctions().At(0).GetParameter(2)
        xmin = -b / (2.*a)
        
        offset =  gr.GetListOfFunctions().At(0).Eval(xmin)
        
        err = sqrt( 2 / a ) / 2.
        sig = sqrt( 2.*(gr.GetListOfFunctions().At(0).Eval(0) - gr.GetListOfFunctions().At(0).Eval(xmin) ) )


        gr2 = ROOT.TGraph()
        for point,val in scan.iteritems():
            nll,stat = val
            if stat != 0: continue
            gr2.SetPoint( gr2.GetN(), options.scanSign*float(point), 2.*(nll-offset) )
        gr2.Sort()
        
        canv = ROOT.TCanvas(fileName,fileName)
        gr2.Fit("pol2")
        gr2.SetMarkerStyle(ROOT.kFullCircle)
        gr2.SetMarkerSize(0.)
        

        self.keep([gr2,canv],format=True)
        ROOT.TGaxis.SetMaxDigits(3)
        gr2.GetXaxis().SetTitle(varName)
        gr2.GetYaxis().SetTitle("-2 #Delta log L")
        gr2.GetYaxis().SetRangeUser(-0.1,1.8)
        gr2.Draw("ap")

        line0 = ROOT.TLine(gr.GetXaxis().GetXmin(),0.,gr.GetXaxis().GetXmax(),0.)
        line0.SetLineColor(ROOT.kBlack)
        line1 = ROOT.TLine(xmin-err,0.,xmin-err,1.)
        line2 = ROOT.TLine(xmin+err,0.,xmin+err,1.)
        for line in line1,line2: line.SetLineColor(ROOT.kRed)
        self.keep( [line0,line1,line2], format=True )
        
        line0.Draw("same")
        line1.Draw("same")
        line2.Draw("same")
        gr2.Draw("p same")
        style_utils.addCmsLumi(canv,2,1,"Unpublished")
        canv.Modified()
        canv.Update()
        
        print xmin, err, sig
        

    def doBins(self,options,args):
        
        if not options.legpos:
            options.legpos = [0.17,0.2,0.65,0.52]

        ### ROOT.cmsTextSize = 0.65
        ### ROOT.relPosY = 0.015
        ### ROOT.extraOverCmsTextSize = 0.7

        netabins = len(options.etabins) - 1
        nptbins  = len(options.ptbins) - 1
        nr9bins  = len(options.r9bins) - 1

        if len(options.groups) > 0:
            categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
        else:
            categories = [ [i] for i in range(options.ncat) ]

        results = None
        if os.path.exists("%s/results.txt" % options.outdir):
            reader = csv.DictReader(open("%s/results.txt" % options.outdir))
            results = {}
            for row in reader:
                srow = {}
                for field,val in row.iteritems():
                    typ = float
                    srow[ field.lstrip(" ").rstrip(" ") ] = val.lstrip(" ").rstrip(" ")
                results[ srow['category'] ] = (srow['eScale'],srow['eer-'])
        print results
        
        nbinsx = nptbins
        nbinsy = nr9bins * netabins

        ybins = []
        ylines = []
        for ibin in range(netabins):
            low = options.etabins[ibin]
            high = options.etabins[ibin+1]
            width = high - low
            step = width / float(nr9bins)
            for ir9 in range(nr9bins):
                ybins.append(low+float(ir9)*step)
            ylines.append( ROOT.TLine(options.ptbins[0],low,options.ptbins[-1],low) )
            
        ylines.append( ROOT.TLine(options.ptbins[0],options.etabins[-1],options.ptbins[-1],options.etabins[-1]) )
        ybins.append(options.etabins[-1])
        xbins = options.ptbins
        print xbins
        print ybins

        hists = []
        hr9 = ROOT.TH1F("hr9","hr9",nr9bins,array.array('d',options.r9bins))
        heta = ROOT.TH1F("heta","heta",netabins,array.array('d',options.etabins))
        palette = [ROOT.kOrange,ROOT.kAzure+1,ROOT.kGreen,ROOT.myColorB2,ROOT.myColorB1]
        ### markers = [ROOT.kFullSquare,ROOT.kFullTriangleUp,ROOT.kFullDiamond,ROOT.kFullCircle]
        markers = [ROOT.kFullSquare,ROOT.kFullTriangleUp,ROOT.kFullSquare,ROOT.kFullCircle]
        ht = ROOT.TH2F("h","h",nbinsx,array.array('d',xbins),nbinsy,array.array('d',ybins))
        ht.SetTitle(";p_{T}(GeV);|#eta| / R_{9}")

        all_graphs = []
        statOnly_graphs = []
        for ieta in range(netabins):
            graphs = []
            sgraphs = []
            for ig in range(nr9bins+1):
                graphs.append( ROOT.TGraphAsymmErrors() )
                graphs[-1].SetLineColor( palette[ig]+2 )
                graphs[-1].SetMarkerColor( palette[ig]+2 )
                ## graphs[-1].SetMarkerStyle( ROOT.kFullCircle )
                graphs[-1].SetFillColor( palette[ig]+2 )
                graphs[-1].SetMarkerStyle( markers[ieta] )
                graphs[-1].SetLineWidth( 2 )
                graphs[-1].SetMarkerSize( 1.5 )
                if ieta == 0 and ig == nr9bins:
                    etaRng = "|#eta| < %1.3g" % ( options.etabins[ieta+2] )
                elif ieta == 0:
                    etaRng = "|#eta| < %1.3g" % ( options.etabins[ieta+1] )
                else:
                    etaRng = "%1.3g < |#eta| < %1.3g" % ( options.etabins[ieta], options.etabins[ieta+1] )
                
                if ig == 0:
                    r9Rng = " R_{9} > %1.3g" % ( options.r9bins[-ig+1] )
                elif ig == nr9bins-1:
                    r9Rng = " R_{9} < %1.3g" % ( options.r9bins[-(ig+1)] )
                elif ig == nr9bins:
                    r9Rng = ""
                else:
                    r9Rng = "%1.3g < R_{9} < %1.3g" % ( options.etabins[ig], options.etabins[ig+1] )
                
                graphs[-1].SetTitle("%s%s" % (etaRng, r9Rng))
                gs = graphs[-1].Clone()
                gs.SetLineColor(palette[ig]+1)                
                gs.SetMarkerSize(0.)
                gs.SetLineStyle(7)
                sgraphs.append(gs)
            all_graphs.append(graphs)
            statOnly_graphs.append(sgraphs)

        all_graphs[0][-1].SetMarkerStyle( markers[-1] )
        all_graphs[2][-1].SetMarkerStyle( markers[-1] )
        statOnly_graphs[0][-1].SetMarkerStyle( markers[-1] )
        statOnly_graphs[2][-1].SetMarkerStyle( markers[-1] )
        style_utils.colors(all_graphs[0][-1]     ,palette[-1])
        style_utils.colors(all_graphs[2][-1]     ,palette[-1])
        style_utils.colors(statOnly_graphs[0][-1],palette[-2])
        style_utils.colors(statOnly_graphs[2][-1],palette[-2])
        statOnly_graphs[0][-1].SetMarkerColor( palette[-1] )
        statOnly_graphs[2][-1].SetMarkerColor( palette[-1] )

        boxes = []
        coords = {}
        for igroup,group in enumerate(categories):
            pairs = []
            minr9 = options.r9bins[-1]
            maxr9 = options.r9bins[0]
            minpt = options.ptbins[-1]
            maxpt = options.ptbins[0]
            mineta = options.etabins[-1]
            maxeta = options.etabins[0]
            miny   = ybins[-1]
            maxy   = ybins[0]
            for cat in group:
                r9bin  = (cat      ) % nr9bins 
                etabin = ((cat / nr9bins)) % netabins
                ptbin  = nptbins  - ((cat / (nr9bins*netabins)) % nptbins) - 1

                minr9  = min( options.r9bins[r9bin], minr9 )
                maxr9  = max( options.r9bins[r9bin+1], maxr9 )
                minpt  = min( options.ptbins[ptbin], minpt )
                maxpt  = max( options.ptbins[ptbin+1], maxpt )
                mineta  = min( options.etabins[etabin], mineta )
                maxeta  = max( options.etabins[etabin+1], maxeta )
                
                xbin = ptbin
                ybin = etabin*nr9bins+r9bin
                x = 0.5*(xbins[xbin] + xbins[xbin+1])
                y = 0.5*(ybins[ybin] + ybins[ybin+1])

                miny  = min( ybins[ybin], miny )
                maxy  = max( ybins[ybin+1], maxy )

                pairs.append( (x,y) )
                
            
            print igroup, minr9, maxr9
            h = ht.Clone("h%d" % igroup)
            if minr9 == options.r9bins[0] and maxr9 == options.r9bins[-1]:
                ihisto = nr9bins
            else:
                ihisto = hr9.FindBin(minr9)-1
            if mineta == options.etabins[0] and maxeta == options.etabins[-1]:
                ieta = netabins
            else:
                ieta = heta.FindBin(mineta)-1
            color = palette[ ihisto ]
            if maxpt >= options.ptbins[-1]:
                color = palette[-2]
            h.SetFillColor(color)
            h.SetFillStyle(1001)
            h.SetMarkerColor(color)
            h.SetLineColor(color)
            print h, color
            hists.append(h)
            print(mineta,minpt,maxeta,maxpt) 
            boxes.append( ROOT.TBox(minpt,mineta,maxpt,maxeta) )
            boxes[-1].SetFillStyle(0)
            boxes[-1].SetLineColor(ROOT.kBlack)
            boxes[-1].SetLineWidth(2)

            boxes.append( ROOT.TBox(minpt,miny,maxpt,maxy) )
            boxes[-1].SetFillStyle(0)
            boxes[-1].SetLineColor(ROOT.kBlack)
            boxes[-1].SetLineStyle(7)
            boxes[-1].SetLineWidth(1)

            for x,y in pairs:
                print x,y,h
                h.Fill(x,y)

            if results:
                statOnly = results[ "%s_statOnly" % options.labels[igroup] ]
                full = results[ "%s" % options.labels[igroup] ]
                gr = all_graphs[ieta][ihisto]
                ip = gr.GetN()
                ## gr.SetPoint(ip, 0.5*(maxpt+minpt), 1.+float(full[0])  )
                gr.SetPoint(ip, 0.5*(maxpt+minpt), float(full[0])  )
                gr.SetPointError(ip, 0.5*(maxpt-minpt), 0.5*(maxpt-minpt), float(full[1]), float(full[1])  )

                gs = statOnly_graphs[ieta][ihisto]
                ip = gs.GetN()
                ## gs.SetPoint(ip, 0.5*(maxpt+minpt), 1.+float(statOnly[0])  )
                gs.SetPoint(ip, 0.5*(maxpt+minpt)+0.5, float(statOnly[0])  )
                gs.SetPointError(ip, 0.5*(maxpt-minpt)+0.5, 0.5*(maxpt-minpt)-0.5, float(statOnly[1]), float(statOnly[1])  )

        canv = ROOT.TCanvas("zmmgBins","zmmgBins")
        hists[0].Draw("box")
        for h in hists[1:]:
            h.Draw("box same")
        for box in boxes:
            box.Draw("same")
        canv.RedrawAxis()
        canv.Modified()
                
        self.keep( [canv,ht] )
        self.keep( hists )
        self.keep( ylines+boxes )

        self.setStyle("*_legend",[["SetTextFont",67],["SetTextSize",22],["SetFillStyle",0],["SetTextAlign",12]]) ## 
        self.setStyle("frame_*",[["xtitle","p_{T} (GeV)"],["ytitle","#delta E_{#gamma} / E_{#gamma}"]])
        canv = ROOT.TCanvas("zmmgFits_eb","zmmgFits_eb")
        frame = ROOT.TH1F("frame_eb","frame_eb",nbinsx+2,array.array('d',[xbins[0]-1.]+xbins+[xbins[-1]+1.]))
        ## frame.GetYaxis().SetRangeUser(1.-2.5e-2,1.+1.e-2)
        frame.GetYaxis().SetRangeUser(-2.5e-2,1.3e-2)
        
        dummy = ROOT.TGraph()
        dummy.SetLineWidth(2)
        dummy_stat = ROOT.TGraph()
        dummy_stat.SetLineStyle(7)
        dummy_stat.SetLineWidth(2)
        extra_legend = ROOT.TLegend(0.22,0.14,0.66,0.2)
        extra_legend.SetName("extra_legend")
        extra_legend.SetNColumns(2)
        extra_legend.AddEntry(dummy,"stat+syst","l")
        extra_legend.AddEntry(dummy_stat,"stat only","l")
        
        self.keep([extra_legend,dummy,dummy_stat],True)

        legend = ROOT.TLegend(*(options.legpos))
        legend.SetName("eb_legend")
        self.keep( [canv,frame,legend], True )
        frame.Draw()
        leglist = {}
        for ibin in range(netabins):
            if options.etabins[ibin+1] > 1.5:
                continue
            
            graphs = all_graphs[ibin]+statOnly_graphs[ibin]
            ### for gr  in graphs:
            ###     if gr.GetN() == 0: continue
            ###     gr.Print()
            ###     gr.SetHistogram(frame)
            ###     gr.Draw("p")
            for grs,opt in [ (statOnly_graphs[ibin],"p"),(all_graphs[ibin],"pe1"), ]:
                for gr  in grs:
                    if gr.GetN() == 0: continue
                    gr.Print()
                    gr.SetHistogram(frame)
                    gr.Draw(opt)
                    ## gr.Draw("p")
                    
            ### for gr in all_graphs[ibin]:
            ###     if gr.GetN() == 0: continue
            ###     legend.AddEntry(gr,"","pe")
            for gr in all_graphs[ibin]:
                if gr.GetN() == 0: continue
                leglist["%f %d %s" % (min([gr.GetX()[ip] for ip in range(gr.GetN())]),ibin,gr.GetTitle())] = gr
            self.keep( graphs )

        print leglist
        keys = sorted(leglist.keys())
        for k in keys:
            legend.AddEntry(leglist[k],"","pe")
                            
            
        legend.Draw("same")
        extra_legend.Draw("same")
        style_utils.addCmsLumi(canv,2,1,"Unpublished")
        canv.RedrawAxis()
        canv.Modified()
        canv.Update()
        
            
        canv = ROOT.TCanvas("zmmgFits_ee","zmmgFits_ee")
        ## frame = ROOT.TH1F("frame_ee","frame_ee",nbinsx,array.array('d',xbins))
        frame = ROOT.TH1F("frame_ee","frame_ee",nbinsx+2,array.array('d',[xbins[0]-1.]+xbins+[xbins[-1]+1.]))
        frame.GetYaxis().SetRangeUser(-4.5e-2,1.6e-2)
        legend = ROOT.TLegend(*(options.legpos))
        legend.SetName("ee_legend")
        self.keep( [canv,frame,legend], True )
        frame.Draw()
        leglist = {}
        for ibin in range(netabins):
            if options.etabins[ibin+1] <= 1.5:
                continue
            graphs = all_graphs[ibin]+statOnly_graphs[ibin]
            ### for gr  in graphs:
            ###     if gr.GetN() == 0: continue
            ###     gr.Print()
            ###     gr.SetHistogram(frame)
            ###     gr.Draw("p")
            for grs,opt in [ (statOnly_graphs[ibin],"p"),(all_graphs[ibin],"pe1"), ]:
                for gr  in grs:
                    if gr.GetN() == 0: continue
                    gr.Print()
                    gr.SetHistogram(frame)
                    gr.Draw(opt)

            for gr in all_graphs[ibin]:
                if gr.GetN() == 0: continue
                leglist["%f %d %s" % (min([gr.GetX()[ip] for ip in range(gr.GetN())]),ibin,gr.GetTitle())] = gr
            self.keep( graphs )

        print leglist
        keys = sorted(leglist.keys())
        for k in keys:
            legend.AddEntry(leglist[k],"","pe")
            
        legend.Draw("same")
        extra_legend.Draw("same")
        style_utils.addCmsLumi(canv,2,1,"Unpublished")
        canv.RedrawAxis()
        canv.Modified()
        canv.Update()

        
if __name__ == "__main__":
    
    app = ZmmgBins()
    app.run()
    
