#!/bin/env python

from pyrapp import *
from optparse import OptionParser, make_option

from copy import copy
from pprint import pprint
import csv, json


# ------------------------------------------------------------------------------------------
class ZmmgApp(PlotApp):

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
            make_option("--label",
                        action="append", dest="labels",
                        default=[],
                        ),
            make_option("--scale-param",
                        action="append", dest="scale_params",
                        default=[],
                        ),
            make_option("-w", "--ws-name",
                        action="store", dest="ws_name",
                        default="cms_hgg_workspace",
                        ),
            make_option("-W","--write-ws",
                        action="store", dest="write_ws", type="string",
                        default=None,
                        ),
            make_option("-o", "--observable",
                        action="store", dest="observable",
                        default="CMS_hgg_mass",
                        ),
            make_option("--obs-bins",
                        action="store", dest="obs_bins", type="int",
                        default=0,
                        ),
            make_option("--obs-scale",
                        action="store", dest="obs_scale", type=float,
                        default=1.,
                        ),
            make_option("--scale-unc",
                        action="callback", callback=optpars_utils.Csv(), dest="scale_unc", type="string",
                        default=None,
                        ),
            make_option("--fit-unc",
                        action="callback", callback=optpars_utils.Csv(), dest="fit_unc", type="string",
                        default=None,
                        ),
            make_option("--plot-nll",
                        action="store_true", dest="plot_nll", 
                        default=False,
                        ),
            make_option("--no-plot-nll",
                        action="store_false", dest="plot_nll", 
                        ),
            make_option("--single-fits",
                        action="store_true", dest="single_fits", 
                        default=False,
                        ),
            make_option("--no-single-fits",
                        action="store_false", dest="single_fits"
                        ),
            make_option("--global-fit",
                        action="store_true", dest="global_fit", 
                        default=True,
                        ),
            make_option("--global-deltanll",
                        action="store_true", dest="global_deltanll", 
                        default=True,
                        ),
            make_option("--no-global-deltanll",
                        action="store_false", dest="global_deltanll", 
                        ),
            make_option("--no-global-fit",
                        action="store_false", dest="global_fit", 
                        ),
            make_option("--bind-shapes",
                        action="store_true", dest="bind_shapes",
                        default=False,
                        ),
            make_option("--scan",action="store",dest="scan", type="string",
                        default=False
                        ),
            make_option("--plot-simultaneous",action="store_true",dest="plot_simultaneous",
                        default=False
                        ),
            make_option("--fix-shapes",action="store_true",dest="fix_shapes",
                        default=False
                        ),
            make_option("-j","--job-id",action="store",dest="job_id", type="int",
                        default=None
                        ),
            make_option("--npoints",action="store",dest="npoints", type="int",
                        default=50
                        ),
            make_option("--first-point",action="store",dest="first_point", type="int",
                        default=None
                        ),
            make_option("--last-point",action="store",dest="last_point", type="int",
                        default=None
                        ),
            make_option("--binned",
                        action="store_true", dest="binned", 
                        default=False,
                        ),
            make_option("--unbinned",
                        action="store_false", dest="binned", 
                        ),
            ]
                                    )
        
        global ROOT, RooFit, style_utils
        import ROOT
        ## ROOT.gSystem.SetIncludePath("-I$ROOTSYS/include -I$ROOFITSYS/include")
        ## ROOT.gSystem.Load("libRooFitCore")
        ## ROOT.gInterpreter.GenerateDictionary("std::map<std::string, RooDataSet*>", "map;string;RooDataSet.h")
        from ROOT import RooFit as RooFit
        import pyrapp.style_utils as style_utils
        
        self.datasets_   = {}
        self.fitCalib_   = {}
        self.calibPdfs_  = {}
        self.results_    = []
        self.nuisParams_ = []
        self.scaleUnc_   = {}
        self.scaleNuis_  = None
        self.fitUnc_     = {}
        self.catScales_  = {}
        
    def getCatName(self,icat, labels=None):
        if labels:
            return labels[icat]
        return "cat%d" % icat

    def readDatasets(self,name,group,igroup,nsig):
        
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
            
        scaleUnc = { nuis.GetName() : 0. for nuis in self.scaleNuis_ }
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
                if ishift == 0:
                    for nu in self.scaleNuis_:
                        scaleUnc[nu.GetName()] += catmc.sumEntries()*self.scaleUnc_[cat][nu.GetName()]
                
                mc[ishift].append(catmc)
        
        for nu in self.scaleNuis_:
            scaleUnc[nu.GetName()] /= mc[0].sumEntries()
        self.scaleUnc_[ name ] = scaleUnc
        ## pprint( self.scaleUnc_ )
        
        self.ws_.rooImport(data)
        for key,val in mc.iteritems():
            self.ws_.rooImport(val)
            
        self.datasets_[ name ] = { "data" : data, "mc" : mc }

    def buildPdf(self,cat,label,param=None,values=None,extra=[],bindTo=None):

        name = "%s_%s" % (cat, label)
        trObs=self.trObs_
        if param:
            if name in self.catScales_:                
                deltaEg = ROOT.RooFormulaVar("deltaEg_%s" % name, "@0", ROOT.RooArgList(self.catScales_[name]))
                ## deltaEg.Print()
            else:
                deltaEg = self.ws_.factory("deltaEg_%s[0.,-1.e-1,1.e-1]" % name)
                self.catScales_[name] = deltaEg                
            lst = ROOT.RooArgList()
            for var in [deltaEg]+extra: lst.add(var)
            mu  = ROOT.RooFormulaVar("mu_%s" % name ,param, lst)
            ## mu.Print()
            self.ws_.rooImport(mu,RooFit.RecycleConflictNodes())
        else:
            mu = self.ws_.factory("mu_%s[1.,0.9,1.1]" % name)
        if bindTo:
            lmbda = ROOT.RooFormulaVar("lmbda_%s" % name ,"@0",ROOT.RooArgList(self.ws_.var("lmbda_%s" % bindTo)))
            sigma = ROOT.RooFormulaVar("sigma_%s" % name ,"@0",ROOT.RooArgList(self.ws_.function("sigma_%s" % bindTo)))
            width = ROOT.RooFormulaVar("width_%s" % name ,"@0",ROOT.RooArgList(self.ws_.var("width_%s" % bindTo)))
            self.ws_.rooImport(lmbda,RooFit.RecycleConflictNodes())
            self.ws_.rooImport(sigma,RooFit.RecycleConflictNodes())
            self.ws_.rooImport(width,RooFit.RecycleConflictNodes())
        else:
            lmbda = self.ws_.factory("lmbda_%s[0.,-10,2]" % name)
            sigma0 = self.ws_.factory("sigma0_%s[2.e-2,1.e-3,2.e-1]" % name)
            ## sigma0 = self.ws_.factory("sigma0_%s[2.e-2,5.e-3,2.e-1]" % name)
	    ## sigmaL = self.ws_.factory("sigmaL_%s[2.e-2,5.e-3,1.e-1]" % name)
	    ## sigmaR = self.ws_.factory("sigmaR_%s[2.e-2,5.e-3,1.e-1]" % name)
            ## sigma0 = ROOT.RooFormulaVar("sigma0_%s" % name, "@0*(@3>@2) + @1*(@3<=@2)",ROOT.RooArgList(sigmaL,sigmaR,mu,trObs))
            lst = ROOT.RooArgList(sigma0,lmbda,trObs)
            sigma = ROOT.RooFormulaVar("sigma_%s" % name ,"@0*(1+exp(@1*(1.-@2)))",lst)
            self.ws_.rooImport(sigma,RooFit.RecycleConflictNodes())
            width = self.ws_.factory("width_%s[3.e-2,1.e-3,2.e-1]" % name)
            ## width = self.ws_.factory("width_%s[3.e-2,1.e-2,2.e-1]" % name)

        shape = self.ws_.factory("Voigtian::shape_%(name)s(%(obs)s,mu_%(name)s,sigma_%(name)s,width_%(name)s)" %
                                 { "name" : name, "obs" : trObs.GetName() }
                                 )
        
        if values and not bindTo:
            vals = copy(values)
            if not param:
                mu.setVal(vals.pop())
            sigma0.setVal(vals.pop())
            lmbda.setVal(vals.pop())
            width.setVal(vals.pop())
            
        ### shape.getDependents(self.ws_.allVars()).Print("V")
        return shape

    def plotFit(self,name,pdf,dataset,style):

        printLevel = ROOT.RooMsgService.instance().globalKillBelow()
        ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

        frame = self.obs_.frame(RooFit.Bins(50))
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

        self.autosave(True)

        ROOT.RooMsgService.instance().setGlobalKillBelow(printLevel)

    def plotNll(self,name,var,logl):
        print( "plotNll", var.GetName() )
        val = var.getVal()
        err = var.getError()
        frame = var.frame(val-2.*err,val+2*err,50)

        for nuis in self.nuisParams_+self.scaleNuis_:
            nuis.setConstant(True)
        logl.plotOn(frame,RooFit.ShiftToZero(),RooFit.LineStyle(ROOT.kDashed))

        for nuis in self.nuisParams_:
            nuis.setConstant(False)
        logl.plotOn(frame,RooFit.ShiftToZero())

        ## for nuis in self.scaleNuis_:
        ##     nuis.setConstant(False)
        ## logl.plotOn(frame,RooFit.ShiftToZero(),RooFit.LineColor(ROOT.kRed))
        
        canv = ROOT.TCanvas("fit_%s" % name,"fit_%s" % name)
        canv.cd()
        frame.Draw()
        
        self.keep( [canv,frame] )

        self.autosave(True)
        
        return frame.getObject(int(frame.numItems()-1))

    def addNuis(self,name,val=None,formula=None,lst=None,offset=-1):
        nu = self.ws_.factory("%s[0,-3,3]" % name)
        nu.setConstant(True)
        if val:
            lst.append(nu)
            formula.append( "%1.4g*@%d" % ( val,len(lst)+offset ) )
            ### print( formula )
        return nu
    
    def calibMcFits(self,cat,nsig,step,bindShapeParams):
        
        self.log("Calibrating energy scale fit in MC for category %s" % cat)
        pdf = self.buildPdf(cat,"mc")

        params = pdf.getDependents(self.ws_.allVars())
        mu     = params["mu_%s_%s" % (cat,"mc") ]
        sigma0 = params["sigma0_%s_%s" % (cat,"mc") ]
        lmbda  = params["lmbda_%s_%s" % (cat,"mc") ]
        width  = params["width_%s_%s" % (cat,"mc") ]

        fitOpts = [RooFit.SumW2Error(True),RooFit.Strategy(1),RooFit.Warnings(False)]
        
        mu.setConstant(True)
        lmbda.setConstant(True)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)

        fitOpts.append(RooFit.Strategy(2))
        mu.setConstant(False)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)

        lmbda.setConstant(False)
        pdf.fitTo(self.datasets_[cat]["mc"][0],RooFit.PrintLevel(-1),*fitOpts)
        
        self.plotFit(name="%s_%s"% (cat,"mc"),pdf=pdf,dataset=self.datasets_[cat]["mc"][0],
                     style=[RooFit.MarkerColor(ROOT.kAzure+2),RooFit.LineColor(ROOT.kAzure+2)])
        
        gr = ROOT.TGraphErrors()
        self.fitCalib_[cat] = gr
        gr.SetPoint(0,0,mu.getVal())
        gr.SetPointError(0,0,mu.getError())
        
        ### start_from = [ mu.getVal(), sigma0.getVal(), lmbda.getVal(), width.getVal() ]
        start_from = [ sigma0.getVal(), lmbda.getVal(), width.getVal() ]
        for ishift in range(-nsig,nsig+1):
            ### if ishift == 0:
            ###     continue
            sigma0.setConstant(True)
            lmbda .setConstant(True)
            width .setConstant(True)

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

        self.log("  Calibration done. Slope is %1.3g +- %1.2g" % (calib.GetParameter(1),calib.GetParError(1)))
        
        self.calibPdfs_[cat] = {}
        nuCalibSlope = self.addNuis("nuisCalibSlope_%s" % cat)
        self.nuisParams_.append(nuCalibSlope)
        extra = []
        self.calibPdfs_[cat]["mc"] = self.buildPdf(cat,"calib_mc","%1.6g + %1.3g*@0" % (calib.GetParameter(0), calib.GetParameter(1)),
                                                   start_from, extra )
        mcDeps = self.calibPdfs_[cat]["mc"].getDependents(self.ws_.allVars())
        deltaEgMC = mcDeps["deltaEg_%s_%s" % (cat,"calib_mc")]
        
        extra = [deltaEgMC]
        form = ["+@1"]
        if cat in self.fitUnc_:
            for nu in self.nuisParams_:
                if nu.GetName() in self.fitUnc_[cat] and self.fitUnc_[cat][nu.GetName()]>0.:
                    self.addNuis(nu.GetName(),self.fitUnc_[cat][nu.GetName()],form,extra,0)
        for nu in self.scaleNuis_:
            self.addNuis(nu.GetName(),self.scaleUnc_[cat][nu.GetName()],form,extra,0)
        extra.append( nuCalibSlope )
        
        if bindShapeParams:
            bindTo = "%s_calib_mc" % cat
        else:
            bindTo = None
        self.calibPdfs_[cat]["data"] = self.buildPdf(cat,"calib_data","%1.6g +(%1.3g+%1.3g*@%d)*(@0%s)" % (calib.GetParameter(0), calib.GetParameter(1),
                                                                                                           calib.GetParError(1),
                                                                                                           len(extra),"+".join(form)),
                                                     start_from,
                                                     extra, bindTo=bindTo
                                                     )
        self.log(" Fit scale dependence for category %s " % cat)
        self.ws_.function("mu_%s_calib_data" % cat).Print("V")

    def fixShapes(self,deps):
        itr = deps.createIterator()
        var = itr.Next()
        while var:
            name = var.GetName()
            if "lmbda" in name or "sigma" in name or "width" in name:
                var.setConstant(True)
            var = itr.Next()
        
    def runFits(self,cat,plot=True,plotNll=False,doStatOnly=True,doScaleFreeze=True):

        pdfs = self.calibPdfs_[cat]
        datasets = self.datasets_[cat]

        paramsData = pdfs["data"].getDependents(self.ws_.allVars())
        paramsMC   = pdfs["mc"].getDependents(self.ws_.allVars())
        
        fitOpts = [RooFit.Strategy(2),RooFit.PrintLevel(-1),RooFit.Warnings(False)]
        ## deltaEgData  = paramsData["deltaEg_%s_%s" % (cat,"calib_data") ]
        deltaEgData = self.catScales_["%s_%s" % (cat,"calib_data")]
        ### sigma0Data   = paramsData["sigma0_%s_%s" % (cat,"calib_data") ]
        ### lmbdaData    = paramsData["lmbda_%s_%s" % (cat,"calib_data") ]
        ### widthData    = paramsData["width_%s_%s" % (cat,"calib_data") ]
        deltaEgMC    = paramsMC["deltaEg_%s_%s" % (cat,"calib_mc") ]

        constraints = ROOT.RooArgSet()
        for nuis in self.nuisParams_+self.scaleNuis_:
            name = nuis.GetName()
            constraints.add( self.ws_.factory("Gaussian::gauss_%(name)s(%(name)s,0.,1.)" % {"name" : name } ) )
            nuis.setConstant(False)
            nuis.setVal(0.)

        ## constraints.Print()
        
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

        simul.getDependents(self.ws_.allVars()).Print("V")
        if constraints.getSize() > 0:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False), RooFit.ExternalConstraints(constraints))
        else:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False))
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)

        minim.migrad()
        minim.minos()
        simul.getDependents(self.ws_.allVars()).Print("V")

        nllMin = nll.getVal()
        
        results = []
        
        results.append( [cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2000. ] )
        
        if doScaleFreeze and len(self.scaleNuis_)>0:
            for nuis in self.scaleNuis_:
                nuis.setConstant(True)
            minim = ROOT.RooMinimizer(nll)
            minim.setPrintLevel(-1)
            minim.setStrategy(2)
            minim.migrad()
            minim.minos()
            simul.getDependents(self.ws_.allVars()).Print("V")
            results.append( ["%s_noEScal" % cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2000. ] )
            
        if doStatOnly and len(self.scaleNuis_+self.nuisParams_)>0:
            for nuis in self.scaleNuis_+self.nuisParams_:
                nuis.setConstant(True)
            minim = ROOT.RooMinimizer(nll)
            minim.setPrintLevel(-1)
            minim.setStrategy(2)
            minim.migrad()
            minim.minos()
            simul.getDependents(self.ws_.allVars()).Print("V")
            results.append( ["%s_statOnly" % cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2000. ] )
            
        for nuis in self.scaleNuis_+self.nuisParams_:
            nuis.setConstant(False)
            
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)
        minim.migrad()
        minim.minos()
        simul.getDependents(self.ws_.allVars()).Print("V")
        results[0][-1] = 2.*(nll.getVal() - nllMin)

        self.results_.extend( results )
        
        self.keep( [simul,combData] )
        
        if plot:
            self.plotFit(name="scale_%s_%s"% (cat,"data"),pdf=pdfs["data"],
                         dataset=self.datasets_[cat]["data"],
                         style=[RooFit.MarkerColor(ROOT.kBlack),RooFit.LineColor(ROOT.kBlack)])
            
            self.plotFit(name="scale_%s_%s"% (cat,"mc"),pdf=pdfs["mc"],
                         dataset=self.datasets_[cat]["mc"][0],
                         style=[RooFit.MarkerColor(ROOT.kRed),RooFit.LineColor(ROOT.kRed)])

            if plotNll:
                pll = nll.createProfile(ROOT.RooArgSet(deltaEgData))
                curve = self.plotNll(name="scale_%s_nll" % cat, var=deltaEgData, logl=pll )
        
        

    def runSimultaneousFit(self,cats,saveTo,plotNll,globalDeltaNll,binned):

        simul = ROOT.RooSimultaneous("model_allcats", "model_allcats", self.cat_)

        constraints = ROOT.RooArgSet()
        for nuis in self.nuisParams_+self.scaleNuis_:
            name = nuis.GetName()
            constraints.add( self.ws_.factory("Gaussian::gauss_%(name)s(%(name)s,0.,1.)" % {"name" : name } ) )
            nuis.setConstant(False)
            nuis.setVal(0.)

        ## dataImport = ROOT.RooArgList()
        dataScales = set()
        index = RooFit.Index(self.cat_)
        obs = ROOT.RooArgSet(self.obs_)
        combData = None
        for cat in cats:
            pdfs = self.calibPdfs_[cat]
            datasets = self.datasets_[cat]

            paramsData = pdfs["data"].getDependents(self.ws_.allVars())
            paramsMc   = pdfs["mc"].getDependents(self.ws_.allVars())
        
            ## deltaEgData  = paramsData["deltaEg_%s_%s" % (cat,"calib_data") ]
            deltaEgMc    = paramsMc["deltaEg_%s_%s" % (cat,"calib_mc") ]
            ##dataScales.append(deltaEgData)
            deltaEgData = self.catScales_["%s_%s" % (cat,"calib_data")] 
            if deltaEgData.IsA().InheritsFrom("RooRealVar"):
                dataScales.add( deltaEgData )
            else:
                deps = deltaEgData.getDependents(self.ws_.allVars())
                itr = deps.createIterator()
                var = itr.Next()
                while var:
                    dataScales.add( var )
                    var = itr.Next()
                    
            simul.addPdf(pdfs["data"],"%s_data" % cat)
            simul.addPdf(pdfs["mc"],"%s_mc" % cat)

            # pre-fit pdfs
            self.log("Pref-fitting category %s" % cat)
            pdfs["mc"].fitTo(self.datasets_[cat]["mc"][0],RooFit.SumW2Error(True),RooFit.Strategy(2),RooFit.PrintLevel(-1))
            ## pdfs["mc"].getDependents(self.ws_.allVars()).Print("V")
            deltaEgMc.setConstant(True)
            pdfs["data"].fitTo(self.datasets_[cat]["data"],RooFit.Strategy(2),RooFit.PrintLevel(-1),
                               RooFit.ExternalConstraints(constraints))
            deltaEgMc.setConstant(False)
            ## pdfs["data"].getDependents(self.ws_.allVars()).Print("V")
            
            self.log(" MC   scale: %1.3g %1.3g %1.3g" % (deltaEgMc.getVal(),deltaEgMc.getErrorHi(),deltaEgMc.getErrorLo()) )
            if deltaEgData.IsA().InheritsFrom("RooRealVar"):
                self.log(" Data scale: %1.3g %1.3g %1.3g" % (deltaEgData.getVal(),deltaEgData.getErrorHi(),deltaEgData.getErrorLo()) )
            else:
                self.log(" Data scale: %1.3g" % (deltaEgData.getVal()) )
            
            if not combData:
                combData = ROOT.RooDataSet("comb_set_allcats","comb_set_allcats", obs,
                                      index,
                                      RooFit.Import("%s_data"% cat,self.datasets_[cat]["data"]),
                                      RooFit.Import("%s_mc"  % cat,self.datasets_[cat]["mc"][0]),
                                       )
            else:
                catData = ROOT.RooDataSet("comb_set_%s" % cat,"comb_set_%s" % cat, obs,
                                          index,
                                          RooFit.Import("%s_data"% cat,self.datasets_[cat]["data"]),
                                          RooFit.Import("%s_mc"  % cat,self.datasets_[cat]["mc"][0]),
                                          )
                combData.append(catData)

                

        ## if fix_shapes:
        ##     self.fixShapes(simul.getDependents(self.ws_.allVars()))

        ## combData.Print("V")
        self.log("Starting global fit ...")
        deps = simul.getDependents(self.ws_.allVars())
        deps.Print("V")
        if binned:
            self.keep(combData)
            combData = combData.binnedClone("comb_set_allcats_binned","comb_set_allcats_binned")
        if constraints.getSize() > 0:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False), RooFit.ExternalConstraints(constraints))
        else:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False))
        
        mcScales = []
        itr = deps.createIterator()
        var = itr.Next()
        while var:
            if "_mc" in var.GetName():
                var.setConstant(True)
                var.Print()
                mcScales.append(var)
            var = itr.Next()

        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)
        print minim.migrad()
        
        for var in mcScales:
            var.setConstant(False)
            
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)
        print minim.migrad()
        
        dataScalesSet = ROOT.RooArgSet()
        for d in dataScales:
            dataScalesSet.add(d)
        ## minim.minos(dataScalesSet)

        self.keep( [simul,combData] )

        if saveTo:
            ## nll.SetName("nll_allcats")
            self.ows_ = ROOT.RooWorkspace("zmmgFit","zmmgFit")
            getattr(self.ows_,"import")(simul)
            getattr(self.ows_,"import")(combData)
            ## getattr(self.ows_,"import")(nll)
            self.ows_.defineSet("constraints",constraints,True)
            self.ows_.defineSet("dataScales",dataScalesSet,True)
            ### self.ows_.saveSnapshot("deltaEgFit",self.ows_.allVars(),True)
            self.ows_.saveSnapshot("deltaEgFit",simul.getDependents(self.ows_.allVars()),True)
            
        self.log("Global fit result")
        simul.getDependents(self.ws_.allVars()).Print("V")
        nllMin = nll.getVal()
                
        for cat in cats:
            pdfs = self.calibPdfs_[cat]
            datasets = self.datasets_[cat]

            self.plotFit(name="scale_simul_%s_%s"% (cat,"data"),pdf=pdfs["data"],
                         dataset=self.datasets_[cat]["data"],
                         style=[RooFit.MarkerColor(ROOT.kBlack),RooFit.LineColor(ROOT.kBlack)])
            
            self.plotFit(name="scale_simul_%s_%s"% (cat,"mc"),pdf=pdfs["mc"],
                         dataset=self.datasets_[cat]["mc"][0],
                         style=[RooFit.MarkerColor(ROOT.kRed),RooFit.LineColor(ROOT.kRed)])
            
        ### for cat,deltaEgData in zip(cats,dataScales):
        ###     pll = nll.createProfile(ROOT.RooArgSet(deltaEgData))
        ###     
        ###     curve = self.plotNll(name="scale_%s_nll" % cat, var=deltaEgData, logl=pll )
        ###     dnll0 = curve.Eval(0.)
        ###     
        ###     self.results_.append( (cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2.*dnll0 ) )
        ###     ## self.results_.append( (cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 1000. ) )
        
        if plotNll:
            self.log("Making profile-likelihood scans")
            for deltaEgData in set(dataScales):
                self.log(" %s ... " % deltaEgData.GetName())
                pll = nll.createProfile(ROOT.RooArgSet(deltaEgData))
                
                curve = self.plotNll(name="%s_nll" % deltaEgData.GetName(), var=deltaEgData, logl=pll )
                dnll0 = curve.Eval(0.)
                
                self.results_.append( (cat, deltaEgData.getVal(), deltaEgData.getErrorLo(), deltaEgData.getErrorHi(), 2.*dnll0 ) )

        if globalDeltaNll:
            self.log("Computing NLL at 0 ...")
            for deltaEgData in dataScales:
                deltaEgData.setVal(0.)
                deltaEgData.setConstant(True)
                
            simul.getDependents(self.ws_.allVars()).Print("V")
            if constraints.getSize() > 0:
                nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False), RooFit.ExternalConstraints(constraints))
            else:
                nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False))
            minim0 = ROOT.RooMinimizer(nll)
            minim0.setPrintLevel(-1)
            minim0.setStrategy(2)
            
            minim0.migrad()
            ## minim0.minos()
            
            if saveTo:
                self.ows_.saveSnapshot("deltaEgZeroFit",self.ows_.allVars(),True)
            dnll0 = 2.*(nll.getVal() - nllMin)
            ndf = len(dataScales)
            prob = ROOT.TMath.Prob(dnll0,ndf)
            ## sig = ROOT.RooStats.PValueToSignificance(prob/2.)
            
            self.results_.append( ("allcats", ndf, prob, 0., dnll0 ) )
        
        if saveTo:
            self.ows_.writeToFile(saveTo,True)
            

    def __call__(self,options,args):
        
        self.loadRootStyle()

        if not options.verbose:
            ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
        
        if options.plot_simultaneous:
            self.plot(options,args)
        elif options.scan:
            print options.scan
            self.scan(options,args)
        else:
            self.fit(options,args)
    

    def plot(self,options,args):
        fin = self.open(options.infile)
        fin.ls()
        self.ws_ = fin.Get("zmmgFit")
        self.obs_ = self.ws_.var(options.observable)
        self.cat_ = self.ws_.cat("zmmgCategory")
        
        simul = self.ws_.pdf("model_allcats")
        if options.binned:
            combData = self.ws_.data("comb_set_allcats_binned")
        else:
            combData = self.ws_.data("comb_set_allcats")
            
        self.ws_.loadSnapshot("deltaEgFit")
        
        if len(options.groups) > 0:
            categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
        else:
            categories = [ [i] for i in range(options.ncat) ]
        
        dataCut   = []
        mcCut     = []
        dataSlice = []
        mcSlice   = []
        dataPdfs  = ROOT.RooArgList()
        mcPdfs    = ROOT.RooArgList()
        dataNorms = ROOT.RooArgList()
        mcNorms   = ROOT.RooArgList()
        for igroup,group in enumerate(categories):
            catName = self.getCatName(igroup,options.labels)
            dataCut.append( "zmmgCategory == zmmgCategory::%s_data" % catName  ) 
            mcCut.append( "zmmgCategory == zmmgCategory::%s_mc" % catName  ) 

            dataSlice.append( "%s_data" % catName  ) 
            mcSlice.append( "%s_mc" % catName  ) 
        
            dataPdf = simul.getPdf("%s_data" % catName)
            mcPdf = simul.getPdf("%s_mc" % catName)
            
            dataDeps = dataPdf.getDependents( self.ws_.allVars() )
            itr = dataDeps.createIterator()
            var = itr.Next()
            while var:
                name = var.GetName()
                if name != self.obs_.GetName():
                    var.setConstant(True)
                var = itr.Next()
            
            mcDeps = mcPdf.getDependents( self.ws_.allVars() )
            itr = mcDeps.createIterator()
            var = itr.Next()
            while var:
                name = var.GetName()
                if name != self.obs_.GetName():
                    var.setConstant(True)
                var = itr.Next()
            
            dataProj = combData.reduce(dataCut[-1])
            dataNorm = self.ws_.factory("%s_dataPdf_norm[%f]" %(catName, dataProj.sumEntries()))
            dataNorm.setConstant(False)
            dataNorm.Print()
            dataExtPdf = ROOT.RooExtendPdf("%s_ext" % dataPdf.GetName(),"%s_ext" % dataPdf.GetName(), dataPdf, dataNorm)
            dataExtPdf.fitTo(dataProj)
            getattr(self.ws_,"import")(dataExtPdf)
            ### dataPdfs.add(dataExtPdf)
            ### dataNorms.add(RooFit.RooConst(1.))
            dataPdfs.add(dataPdf)
            dataNorms.add(dataNorm)
            dataNorm.Print()
            
            self.keep( [dataNorm, dataExtPdf] )

            mcProj = combData.reduce(mcCut[-1])
            mcNorm = self.ws_.factory("%s_mcPdf_norm[%f]" % (catName,mcProj.sumEntries()))
            mcNorm.setConstant(False)
            mcExtPdf = ROOT.RooExtendPdf("%s_ext" % mcPdf.GetName(),"%s_ext" % mcPdf.GetName(), mcPdf, mcNorm)
            mcExtPdf.fitTo(mcProj)
            ## mcPdfs.add(mcExtPdf)
            ## mcNorms.add(RooFit.RooConst(1.))
            getattr(self.ws_,"import")(mcExtPdf)
            mcPdfs.add(mcPdf)
            mcNorms.add(mcNorm)
            mcNorms.Print()

            self.keep( [mcNorm, mcExtPdf] )
            
        dataPdf = ROOT.RooAddPdf("data_pdf","data_pdf",dataPdfs,mcNorms)
        mcPdf = ROOT.RooAddPdf("mc_pdf","mc_pdf",mcPdfs,mcNorms)
        
        self.keep( [dataPdf, mcPdf] )

        dataCut = "||".join( dataCut )
        mcCut   = "||".join( mcCut )

        dataSlice = ",".join( dataSlice )
        mcSlice   = ",".join( mcSlice )
        
        print dataCut, dataSlice
        print mcCut, mcSlice
        
        printLevel = ROOT.RooMsgService.instance().globalKillBelow()
        ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
        legStyle  = [["SetTextFont",67],["SetTextSize",17],["SetFillStyle",0],["SetTextAlign",12]]
                
        style=[RooFit.MarkerColor(ROOT.kBlack),RooFit.LineColor(ROOT.kBlack),RooFit.Precision(1.e-9),RooFit.LineWidth(3),RooFit.MarkerSize(1.4)]
        
        ## xaxisStyle = [("SetTitle","s_{E^{#gamma}}"),("UseCurrentStyle"),("SetRangeUser",(0.5,1.5))]
        xaxisStyle = [("SetTitle","s_{E_{#gamma}} = (m_{#mu#mu#gamma}^{2} - m_{#mu#mu}^{2}) / (m_{Z}^{2} - m_{#mu#mu}^{2})"),("UseCurrentStyle"),("SetRangeUser",(0.5,1.5))]
        yaxisStyle = [("SetTitle","Events / %1.2g" % ( (self.obs_.getMax()-self.obs_.getMin())/50.) ),("UseCurrentStyle"),("SetRangeUser",(0.,5000.))]
        
        frame = self.obs_.frame(RooFit.Bins(50))
        
        dataProj = combData.reduce(RooFit.Cut(dataCut))
        dataProj.plotOn(frame,*style)
        dataPdf.plotOn(frame,*style)
        dataFit  = frame.getObject(int(frame.numItems()-2))
                
        ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
        
        style=[RooFit.MarkerColor(ROOT.kAzure+2),RooFit.LineColor(ROOT.kAzure+2),RooFit.Precision(1.e-9),RooFit.LineWidth(3),RooFit.LineStyle(7),RooFit.MarkerSize(1.4),RooFit.MarkerStyle(ROOT.kOpenTriangleUp)]
        
        mcProj = combData.reduce(RooFit.Cut(mcCut))
        scl = 0.995
        scl = 2.65e+04/ dataProj.sumEntries()
        ## print scl
        mcProj.plotOn(frame,*style+[RooFit.Rescale(scl*dataProj.sumEntries() / mcProj.sumEntries())])
        mcPdf.plotOn(frame,*style+[RooFit.Normalization(scl*dataProj.sumEntries() / mcProj.sumEntries())])
        mcFit  = frame.getObject(int(frame.numItems()-2))
        
        canv = ROOT.TCanvas("combfit_plot")
        canv.cd()
        frame.Draw()

        legend = ROOT.TLegend(0.65,0.55,0.9,0.95)
        legend.AddEntry(None,"Z#rightarrow#mu#mu#gamma","")
        legend.AddEntry(dataFit,"Data","pe")
        legend.AddEntry(mcFit,"Simulation","pe")

        style_utils.apply(legend,legStyle)
        style_utils.apply(frame.GetXaxis(),xaxisStyle)
        style_utils.apply(frame.GetYaxis(),yaxisStyle)
        legend.Draw("same")

        canv.Modified()
        canv.Update()
        style_utils.addCmsLumi(canv,2,1,"Unpublished")

        self.keep( [canv,frame,legend,dataFit,mcFit] )
        
        ### dataHist = frameData.getObject(int(frameData.numItems()-2)).Clone()
        ### dataFit  = frameData.getObject(int(frameData.numItems()-1)).Clone()
        ### 
        ### mcHist = frameMc.getObject(int(frameMc.numItems()-2)).Clone()
        ### mcFit  = frameMc.getObject(int(frameMc.numItems()-1)).Clone()
        ### 
        ### frameBoth = frameData.emptyClone("combfit_plot")
        ### 
        ### canvBoth = ROOT.TCanvas("combfit_plot")
        ### canvBoth.cd()
        ### 
        ### for ob in dataHist,dataFit,mcHist,mcFit:
        ###     frameBoth.addObject(ob)
        ### frameBoth.Draw()
        ### 
        ### self.keep( [dataHist,dataFit,mcHist,mcFit,frameBoth,canvBoth] )
        
        #### frameResid = self.obs_.frame()
        #### hist = frame.getObject(int(frame.numItems()-2))
        #### fit  = frame.getObject(int(frame.numItems()-1))
        #### resid = frame.residHist(hist.GetName(),fit.GetName(),True)
        #### resid.SetMarkerColor(hist.GetMarkerColor())
        #### resid.SetLineColor(hist.GetLineColor())
        #### frameResid.addPlotable(resid,"PE")
        #### 
        #### canv = ROOT.TCanvas("fit_%s" % name )
        #### canv.Divide(1,2)
        #### canv.cd(1)
        #### ROOT.gPad.SetPad(0.,0.2,1.,1.)
        #### canv.cd(2)
        #### ROOT.gPad.SetPad(0.,0.,1.,0.2)
        #### 
        #### canv.cd(1)
        #### frame.GetYaxis().SetLabelSize( frame.GetYaxis().GetLabelSize() * canv.GetWh() / ROOT.gPad.GetWh() )
        #### frame.Draw()
        #### canv.cd(2)
        #### ROOT.gPad.SetGridy()
        #### frameResid.Draw()
        #### frameResid.GetYaxis().SetLabelSize( frameResid.GetYaxis().GetLabelSize() * 3.5 )
        #### frameResid.GetYaxis().SetTitle("pull")
        #### 
        #### self.keep( [canv,frame,frameResid] )

        self.autosave(True)

        ROOT.RooMsgService.instance().setGlobalKillBelow(printLevel)
        

        
    def scan(self,options,args):
        fin = self.open(options.infile)
        self.ws_ = fin.Get("zmmgFit")

        print options.scan
        
        var = options.scan
        rng = None
        if "[" in var:
            var,rng = var.split("[")
        self.var_ = self.ws_.var(var)
        if rng:
            rng = [ float(t) for t in rng.rstrip("]").split(",") ]
            ## self.var_.setRange(rngMin,rngMax)
        else:
            rng = [ self.var_.getMin(), self.var_.getMax() ]

        self.var_.Print()

        simul = self.ws_.pdf("model_allcats")
        if options.binned:
            combData = self.ws_.data("comb_set_allcats_binned")
        else:
            combData = self.ws_.data("comb_set_allcats")
        constraints = self.ws_.set("constraints")
        
        ## if fix_shapes:
        ##     self.fixShapes(simul.getDependents(self.ws_.allVars()))
            
        combData.Print()
        constraints.Print()

        if constraints.getSize() > 0:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False), RooFit.ExternalConstraints(constraints))
        else:
            nll = simul.createNLL(combData, RooFit.NumCPU(8), RooFit.Extended(False))

        nll.enableOffsetting(True)
        values = {}

        self.ws_.loadSnapshot("deltaEgFit")
        self.var_.Print()        

        self.var_.setConstant(False)
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)
        minim.optimizeConst(True)
        st = minim.migrad()

        nll0 = nll.getVal()
        self.var_.Print()
        
        self.var_.setConstant(True)
        minim = ROOT.RooMinimizer(nll)
        minim.setPrintLevel(-1)
        minim.setStrategy(2)
        minim.optimizeConst(True)
        ## st = minim.migrad()
        ## st = 200
        
        self.var_.Print()
        pll = nll ## .createProfile(ROOT.RooArgSet(self.var_))
        ## print pll.minimizer().fitter().Result().Status() 
        values[self.var_.getVal()] = ( pll.getVal(),st )
        print( self.var_.getVal(), values[self.var_.getVal()], nll.getVal()-nll0 )
        
        step = (rng[1] - rng[0])/ float(options.npoints-1)
        first = 0
        last = options.npoints
        if options.first_point:
            first = options.first_point
            last  = options.last_point
        print first, last
        for ip in range(first,last):
            point = rng[0] + step*float(ip)
            nll.enableOffsetting(True)
            self.var_.setVal(point)
            st = minim.migrad()
            values[point] = (pll.getVal(),st)
            print( point, values[point], nll.getVal()-nll0 )

        outname = "scan_%s" % self.var_.GetName()
        if self.options.job_id != None:
            outname += "_%d" % self.options.job_id
        outfile = open("%s/%s.json" % (self.options.outdir,outname), "w+")
        outfile.write( json.dumps( values,indent=4,sort_keys=True) )
        outfile.close()
        
        
    def fit(self,options,args):
        fin = self.open(options.infile)
        
        self.ws_ = fin.Get(options.ws_name)
        self.ws_.rooImport = lambda *args : getattr(self.ws_,"import")(*args) 
        self.obs_ = self.ws_.var(options.observable)
        if options.obs_bins > 0:
            self.obs_.setBins(options.obs_bins)
        self.scaleObs_ = options.obs_scale
        obs = ROOT.RooArgList(self.obs_)
        self.trObs_ = ROOT.RooFormulaVar("zmmgObs","@0/%1.4g" % self.scaleObs_,obs)
        self.ws_.rooImport(self.trObs_)
        ## self.obs_.setRange(0.6,1.4)
        self.cat_ = ROOT.RooCategory("zmmgCategory","Zmmg Category")
        self.ws_.rooImport(self.cat_)

        if options.scale_unc:
            for row in options.scale_unc:
                srow = {}
                for field,val in row.iteritems():
                    typ = float
                    if "cat" in field:
                        typ = int
                    srow[ field.lstrip(" ").rstrip(" ") ] = typ(val)
                self.scaleUnc_[ srow["cat"] ] = srow
                if not self.scaleNuis_:
                    self.scaleNuis_ = []
                    for n in srow.keys():
                        if n!="cat" and n!="tot":
                            self.scaleNuis_.append( self.addNuis(n) )
        else:
            self.scaleNuis_ = []

        if options.fit_unc:
            for row in options.fit_unc:
                srow = {}
                for field,val in row.iteritems():
                    typ = float
                    if "cat" in field:
                        typ = str
                    srow[ field.lstrip(" ").rstrip(" ") ] = typ(val)
                self.fitUnc_[ srow["cat"] ] = srow
                if not self.nuisParams_:
                    self.nuisParams_ = []
                    for n in srow.keys():
                        if n!="cat" and n!="tot":
                            self.nuisParams_.append( self.addNuis(n) )
        else:
            self.nuisParams_ = []
            
        if len(options.groups) > 0:
            categories = [ [int(t) for t in g.split(",")] for g in options.groups ]
        else:
            categories = [ [i] for i in range(options.ncat) ]
        
        allcats = []    
        for igroup,group in enumerate(categories):
            catName = self.getCatName(igroup,options.labels)

            if len(options.scale_params)>0:
                if len(options.scale_params) == 1:
                    catScale = options.scale_params[0]
                else:
                    catScale = options.scale_params[igroup]
                if "=" in catScale:
                    name,df = [ a.rstrip(" ").lstrip(" ") for a in catScale.split("=") ]
                    formula,deps = [ a.rstrip(" ").lstrip(" ") for a in df.split(";") ]
                    rooDeps = ROOT.RooArgList()
                    for dep in deps.split(","):
                        var = self.ws_.factory("%s[0.,-1.e-1,1.e-1]"%dep.rstrip(" ").lstrip(" "))
                        rooDeps.add(var)
                    scaleParam = ROOT.RooFormulaVar(name,formula,rooDeps)
                    self.log("Scale parameter for category %s" % catName)
                    scaleParam.Print()
                    self.ws_.rooImport(scaleParam)
                else:
                    scaleParam = self.ws_.factory("%s[0.,-1.e-1,1.e-1]"%catScale)
                self.catScales_["%s_calib_data"%catName] = scaleParam
                ## print self.catScales_
                
            self.readDatasets(catName,group,igroup,options.nsigma)
            self.calibMcFits(catName,options.nsigma,options.step,options.bind_shapes)

            if options.single_fits:
                self.runFits(catName,True,options.plot_nll)
            allcats.append(catName)

        if options.global_fit:
            self.runSimultaneousFit(allcats,options.write_ws,options.plot_nll,options.global_deltanll,options.binned)
        
        ## pprint( self.results_ )
        out = open("%s/results.txt" % options.outdir,"w+")
        out.write( "category,".ljust(25)+
                   "eScale,".ljust(13)+
                   "err+,".ljust(13)+
                   "eer-,".ljust(13)+
                   "-2DeltaLL(0),".ljust(13)+
                   "\n"
                   )
        
        for line in self.results_:
            out.write(("%s,"%line[0]).ljust(25))
            for field in line[1:]:
                out.write(("%1.3g," % field).ljust(13))
            out.write("\n")
        out.close()
        out = open("%s/results.txt" % options.outdir)
        print out.read()
        
if __name__ == "__main__":
    
    app = ZmmgApp()
    app.run()
    

#  LocalWords:  TCanvas
