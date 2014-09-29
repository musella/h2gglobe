#!/bin/env python

from pyrapp import *
from optparse import OptionParser, make_option

from copy import copy
from pprint import pprint

# ------------------------------------------------------------------------------------------
class ZmmgApp(PyRApp):

    def __init__(self):
        super(ZmmgApp,self).__init__(option_list=[
            make_option("-s", "--step",
                        action="store", type="float", dest="step",
                        default=2e-3,
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
            make_option("-i", "--infile",
                        action="store", type="str", dest="infile",
                        default="",
                        ),
            make_option("-w", "--ws-name",
                        action="append", dest="ws_name",
                        default="cms_hgg_workspace",
                        ),
            make_option("-o", "--observable",
                        action="append", dest="observable",
                        default="CMS_hgg_mass",
                        ),
            ]
                                    )

        global ROOT, RooFit, style_utils
        import ROOT
        from ROOT import RooFit as RooFit
        import pyrapp.style_utils as style_utils

        self.datasets_  = {}
        self.fitCalib_  = {}
        self.calibPdfs_ = {}
        self.results_   = []
        
    def getCatName(self,icat, labels=None):
        if labels:
            return labels[icat]
        return "cat%d" % icat

    def readDatasets(self,name,group,nsig):
        
        self.cat_.defineType("%s_data" % name)
        self.cat_.defineType("%s_mc" % name)

        data = ROOT.RooDataSet("data_%s" % name, "data_%s" % name, ROOT.RooArgSet(self.obs_) )
        mc   = {}
        for ishift in range(-nsig,nsig+1):
            shift = ""
            if ishift > 0:
                shift = "_shift_up%d" % ishift
            elif ishift < 0:
                shift = "_shift_down%d" % -ishift
            mc[ishift] = ROOT.RooDataSet("mc_%s%s" % (name, shift), "mc_%s%s" % (name, shift), ROOT.RooArgSet(self.obs_) )
            
        for cat in group:
            catdata = self.ws_.data("data_mass_cat%d" % cat)
            data.append(catdata)

            for ishift in range(-nsig,nsig+1):
                label = ""
                if ishift > 0:
                    label = "_E_scaleUp%02d_sigma" % ishift
                elif ishift < 0:
                    label = "_E_scaleDown%02d_sigma" % -ishift
                catmc   = self.ws_.data("sig_dymm_mass_m90_cat%d%s" % (cat,label))
                
                mc[ishift].append(catmc)
        self.ws_.rooImport(data)
        for key,val in mc.iteritems():
            self.ws_.rooImport(val)
            
        self.datasets_[ name ] = { "data" : data, "mc" : mc }

    def buildPdf(self,cat,label,param=None,values=None,extra=None):

        name = "%s_%s" % (cat, label)

        lmbda = self.ws_.factory("lmbda_%s[0.,-10,0]" % name)
        if param:
            deltaEg = self.ws_.factory("deltaEg_%s[0.,-1.e-1,1.e-1]" % name)
            if extra:
                lst = ROOT.RooArgList(deltaEg,*extra)
            else:
                lst = ROOT.RooArgList(deltaEg)
            mu  = ROOT.RooFormulaVar("mu_%s" % name ,param, lst)
            ## mu.Print()
            self.ws_.rooImport(mu)
        else:
            mu = self.ws_.factory("mu_%s[1.,0.9,1.1]" % name)
	sigma0 = self.ws_.factory("sigma0_%s[2.e-2,5.e-3,2.e-1]" % name)
	## sigmaL = self.ws_.factory("sigmaL_%s[2.e-2,5.e-3,1.e-1]" % name)
	## sigmaR = self.ws_.factory("sigmaR_%s[2.e-2,5.e-3,1.e-1]" % name)
        ## sigma0 = ROOT.RooFormulaVar("sigma0_%s" % name, "@0*(@3>@2) + @1*(@3<=@2)",ROOT.RooArgList(sigmaL,sigmaR,mu,self.obs_))
	lst = ROOT.RooArgList(sigma0,lmbda,self.obs_)
	sigma = ROOT.RooFormulaVar("sigma_%s" % name ,"@0*(1+exp(@1*(1.-@2)))",lst)
        self.ws_.rooImport(sigma)
        
	width = self.ws_.factory("width_%s[3.e-2,1.e-2,2.e-1]" % name)
        shape = self.ws_.factory("Voigtian::shape_%(name)s(%(obs)s,mu_%(name)s,sigma_%(name)s,width_%(name)s)" %
                                 { "name" : name, "obs" : self.obs_.GetName() }
                                 )
        
        if values:
            vals = copy(values)
            if not param:
                mu.setVal(vals.pop())
            sigma0.setVal(vals.pop())
            lmbda.setVal(vals.pop())
            width.setVal(vals.pop())
            
        ### shape.getDependents(self.ws_.allVars()).Print("V")
        return shape

    def plotFit(self,name,pdf,dataset,style):
        
        frame = self.obs_.frame()
        dataset.plotOn(frame,*style)
        pdf.plotOn(frame,*style)

        frameResid = self.obs_.frame()
        hist = frame.getObject(int(frame.numItems()-2))
        fit  = frame.getObject(int(frame.numItems()-1))
        resid = frame.residHist(hist.GetName(),fit.GetName(),True)
        resid.SetMarkerColor(hist.GetMarkerColor())
        resid.SetLineColor(hist.GetLineColor())
        frameResid.addPlotable(resid,"PE")
        
        canv = ROOT.TCanvas("fit_%s" % name )
        canv.Divide(1,2)
        canv.cd(1)
        ROOT.gPad.SetPad(0.,0.2,1.,1.)
        canv.cd(2)
        ROOT.gPad.SetPad(0.,0.,1.,0.2)

        canv.cd(1)
        frame.GetYaxis().SetLabelSize( frame.GetYaxis().GetLabelSize() * canv.GetWh() / ROOT.gPad.GetWh() )
        frame.Draw()
        canv.cd(2)
        ROOT.gPad.SetGridy()
        frameResid.Draw()
        frameResid.GetYaxis().SetLabelSize( frameResid.GetYaxis().GetLabelSize() * 3.5 )
        frameResid.GetYaxis().SetTitle("pull")

        self.keep( [canv,frame,frameResid] )

    def plotNll(self,name,var,logl):
        val = var.getVal()
        err = var.getError()
        frame = var.frame(val-2.*err,val+2*err)
        logl.plotOn(frame,RooFit.ShiftToZero())
        
        canv = ROOT.TCanvas("fit_%s" % name,"fit_%s" % name)
        canv.cd()
        frame.Draw()
        
        self.keep( [canv,frame] )

        return frame.getObject(int(frame.numItems()-1))
                
    def calibMcFits(self,cat,nsig,step):
        pdf = self.buildPdf(cat,"mc")

        params = pdf.getDependents(self.ws_.allVars())
        mu     = params["mu_%s_%s" % (cat,"mc") ]
        sigma0 = params["sigma0_%s_%s" % (cat,"mc") ]
        lmbda  = params["lmbda_%s_%s" % (cat,"mc") ]
        width  = params["width_%s_%s" % (cat,"mc") ]

        fitOpts = [RooFit.SumW2Error(True),RooFit.Strategy(1)]
        
        mu.setConstant(True)
        lmbda.setConstant(True)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)

        mu.setConstant(False)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)

        fitOpts.append(RooFit.Strategy(2))
        lmbda.setConstant(False)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)

        self.plotFit(name="%s_%s"% (cat,"mc"),pdf=pdf,dataset=self.datasets_[cat]["mc"][0],
                     style=[RooFit.MarkerColor(ROOT.kBlue),RooFit.LineColor(ROOT.kBlue)])
        
        gr = ROOT.TGraphErrors()
        self.fitCalib_[cat] = gr
        gr.SetPoint(0,0,mu.getVal())
        gr.SetPointError(0,0,mu.getError())
        
        ### start_from = [ mu.getVal(), sigma0.getVal(), lmbda.getVal(), width.getVal() ]
        start_from = [ sigma0.getVal(), lmbda.getVal(), width.getVal() ]
        for ishift in range(-nsig,nsig+1):
            if ishift == 0:
                continue
            pdf.fitTo(self.datasets_[cat]["mc"][ishift],RooFit.PrintLevel(-1),*fitOpts)

            ip = gr.GetN()
            gr.SetPoint(ip,float(ishift)*step,mu.getVal())
            gr.SetPointError(ip,0.,mu.getError())

        canvCalib = ROOT.TCanvas("fit_%s_calib" %cat, "fit_%s_calib" %cat)
        ROOT.gStyle.SetOptFit(1)
        gr.Fit("pol1","Q+")
        gr.Draw("AP")
        gr.SetTitle(";#Delta E_{gamma}; #Delta mu_{s}")
        calib = gr.GetListOfFunctions().At(0)
        self.keep( [canvCalib,gr] )

        self.calibPdfs_[cat] = {}
        self.calibPdfs_[cat]["mc"] = self.buildPdf(cat,"calib_mc","%1.6g + @0*%1.3g" % (calib.GetParameter(0), calib.GetParameter(1)), start_from )
        mcDeps = self.calibPdfs_[cat]["mc"].getDependents(self.ws_.allVars())
        mcDeps.Print()
        deltaEgMC = mcDeps["deltaEg_%s_%s" % (cat,"calib_mc")]
        
        self.calibPdfs_[cat]["data"] = self.buildPdf(cat,"calib_data","%1.6g + (@0+@1)*%1.3g" % (calib.GetParameter(0), calib.GetParameter(1)), start_from,
                                                     [deltaEgMC]
                                                     )
        ### self.calibPdfs_[cat] = { "mc" : self.buildPdf(cat,"calib_mc",values=start_from ),
        ###                          "data" : self.buildPdf(cat,"calib_data",values=start_from )
        ###                          }

    def runFits(self,cat):

        pdfs = self.calibPdfs_[cat]
        datasets = self.datasets_[cat]

        paramsData = pdfs["data"].getDependents(self.ws_.allVars())
        paramsMC   = pdfs["mc"].getDependents(self.ws_.allVars())

        fitOpts = [RooFit.Strategy(2),RooFit.PrintLevel(-1)]
        deltaEgData  = paramsData["deltaEg_%s_%s" % (cat,"calib_data") ]
        sigma0Data   = paramsData["sigma0_%s_%s" % (cat,"calib_data") ]
        lmbdaData    = paramsData["lmbda_%s_%s" % (cat,"calib_data") ]
        widthData    = paramsData["width_%s_%s" % (cat,"calib_data") ]
        deltaEgMC    = paramsMC["deltaEg_%s_%s" % (cat,"calib_mc") ]

        ### self.results_[cat] = []
        ### sigma0Data .setConstant(True)
        ### lmbdaData  .setConstant(True)
        ### widthData  .setConstant(True)
        ### pdfs["data"].fitTo(self.datasets_[cat]["data"],*fitOpts)
        ### self.results_[cat].append( (deltaEgData.getVal(),deltaEgData.getError()) )
        ### 
        ### sigma0Data .setConstant(False)
        ### lmbdaData  .setConstant(False)
        ### widthData  .setConstant(False)
        ### pdfs["data"].fitTo(self.datasets_[cat]["data"],*fitOpts)
        ### self.plotFit(name="scale_%s_%s"% (cat,"data"),pdf=pdfs["data"],
        ###              dataset=self.datasets_[cat]["data"],
        ###              style=[RooFit.MarkerColor(ROOT.kBlack),RooFit.LineColor(ROOT.kBlack)])
        ### 
        ### fitOpts.append( RooFit.SumW2Error(1) )
        ### pdfs["mc"].fitTo(self.datasets_[cat]["mc"][0],*fitOpts)
        ### 
        ### self.plotFit(name="scale_%s_%s"% (cat,"mc"),pdf=pdfs["mc"],
        ###              dataset=self.datasets_[cat]["mc"][0],
        ###              style=[RooFit.MarkerColor(ROOT.kRed),RooFit.LineColor(ROOT.kRed)])
        ### 
        ### ## paramsData.Print("V")
        ### ## paramsMC.Print("V")
        ### 
        ### self.results_[cat].extend( [ (deltaEgData.getVal(),deltaEgData.getError()), (deltaEgMC.getVal(),deltaEgMC.getError()) ] )

        simul = ROOT.RooSimultaneous("model_%s" % cat, "model_%s" % cat, self.cat_)
        simul.addPdf(pdfs["data"],"%s_data" % cat)
        simul.addPdf(pdfs["mc"],"%s_mc" % cat)
        
        index = RooFit.Index(self.cat_)
        obs = ROOT.RooArgSet(self.obs_)
        combData = ROOT.RooDataSet("comb_set_%s" % cat,"comb_set_%s" % cat, obs,
                                   index,
                                   RooFit.Import("%s_data"% cat,self.datasets_[cat]["data"]),
                                   RooFit.Import("%s_mc"  % cat,self.datasets_[cat]["mc"][0]),
                                   )

        nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False))
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)

        minim.migrad()
        minim.minos()

        pll = nll.createProfile(ROOT.RooArgSet(deltaEgData))
        self.keep( [simul,combData] )
        
        self.plotFit(name="scale_%s_%s"% (cat,"data"),pdf=pdfs["data"],
                     dataset=self.datasets_[cat]["data"],
                     style=[RooFit.MarkerColor(ROOT.kBlack),RooFit.LineColor(ROOT.kBlack)])

        self.plotFit(name="scale_%s_%s"% (cat,"mc"),pdf=pdfs["mc"],
                     dataset=self.datasets_[cat]["mc"][0],
                     style=[RooFit.MarkerColor(ROOT.kRed),RooFit.LineColor(ROOT.kRed)])
        
        curve = self.plotNll(name="scale_%s_nll" % cat, var=deltaEgData, logl=pll )
        nll0 = curve.Eval(0.)
        
        self.results_.append( (cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2.*nll0 ) )
        
                                   
    def __call__(self,options,args):

        fin = self.open(options.infile)
        
        self.ws_ = fin.Get(options.ws_name)
        self.ws_.rooImport = lambda *args : getattr(self.ws_,"import")(*args) 
        self.obs_ = self.ws_.var(options.observable)
        self.cat_ = ROOT.RooCategory("zmmgCategory","Zmmg Category")
        self.ws_.rooImport(self.cat_)

        if not options.verbose:
            ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
        
        if len(options.groups) > 0:
            categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
        else:
            categories = [ [i] for i in range(options.ncat) ]
        
            
        for igroup,group in enumerate(categories):
            catName = self.getCatName(igroup,options.labels)

            self.readDatasets(catName,group,options.nsigma)
            self.calibMcFits(catName,options.nsigma,options.step)
            
            self.runFits(catName)

        ## pprint( self.results_ )
        out = open("%s/results.txt" % options.outdir,"w+")
        out.write( "category".ljust(25)+
                   "eScale".ljust(13)+
                   "err+".ljust(13)+
                   "eer-".ljust(13)+
                   "-2DeltaLL(0)".ljust(13)+
                   "\n"
                   )
        
        for line in self.results_:
            out.write(line[0].ljust(25))
            for field in line[1:]:
                out.write(("%1.3g" % field).ljust(13))
            out.write("\n")
        out.close()
        out = open("%s/results.txt" % options.outdir)
        print out.read()
        
if __name__ == "__main__":

    app = ZmmgApp()
    app.run()
    
