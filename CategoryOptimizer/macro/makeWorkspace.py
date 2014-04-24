#!/bin/env python

import sys, types, os
import numpy
from math import sqrt, log
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.3f')

## from plotVbfVar import *

from optparse import OptionParser, make_option
from  pprint import pprint

objs = []

##
def mkpol(ord,cat,ws,var="CMS_hgg_mass"):
    norms = []
    pdfs = []
    for i in range(ord+1):
        norm = ws.factory("pol%d_coeff%d_cat%d[0.1,-1,1.]" % (ord,i,cat) )
        objs.append(norm)
        norm2 = ROOT.RooFormulaVar("pol%d_sqcoeff%d_cat%d" % (ord,i,cat),"pol%d_sqcoeff%d_cat%d" % (ord,i,cat),
                               "@0*@0", ROOT.RooArgList(norm) )
        norms.append(norm2)

    names = {
        "cat" : cat,
        "ord" : ord,
        "var" : var
        }
    pdf = ROOT.RooBernstein("pol%(cat)d_%(ord)d" % names,  "pol%(cat)d_%(ord)d" % names,
                            ws.var(var), ROOT.RooArgList(*norms) )
    pdfs.append(pdf)
    objs.append( [pdf, norms] )
    return [ROOT.RooFit.RooConst(1.)], pdfs 

##
def mkPdf(name,ord,cat,ws):
    norms, pdfs = globals()["mk%s" % name](ord,cat,ws)

    try:
        norms[0].setVal(1.)
        norms[0].setConstant(True)
    except:
        pass
    
    pdf = ROOT.RooAddPdf("%s%d_cat%d_pdf" % (name,ord,cat), "%s%d_cat%d_pdf" % (name,ord,cat), ROOT.RooArgList(*pdfs), ROOT.RooArgList(*norms) )

    norm = ws.factory("model_cat%d_norm[0,1.e+6]" % (cat))
    ## extpdf = ROOT.RooExtendPdf("%s%d_cat%d_extpdf" % (name,ord,cat), "%s%d_cat%d_extpdf" % (name,ord,cat), pdf, norm)
    extpdf = ROOT.RooExtendPdf("model_cat%d" % (cat), "model_cat%d" % (cat), pdf, norm)
    getattr(ws,"import")(pdf, ROOT.RooFit.RecycleConflictNodes())
    getattr(ws,"import")(extpdf, ROOT.RooFit.RecycleConflictNodes())
    
    objs.append( [pdf, extpdf] )

    ## extpdf = pdf
    ## getattr(ws,"import")(pdf, ROOT.RooFit.RecycleConflictNodes())
    
    objs.append( [pdf, extpdf] )

    return extpdf

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
        
    fin = ROOT.TFile.Open(options.file)

    samples = { "sig" : ["sigRv","sigWv"] , "bkg" : ["bkg"] }
    trees = {}

    catdef = open(options.catdef)
    summary = json.loads(catdef.read())

    obsname,obsmin,obsmax = options.observable
    nbins = options.nbins
    binsize = (obsmax - obsmin) / float(nbins)
    varnames = options.variables
    
    cats = summary[options.ncat]["boundaries"]
    print cats
    ncat = int(options.ncat)
    
    poly = [ 20, 200, 10000, 20000, 40000 ]
    
    nvars = len(varnames)
    bounds = [ [ float(cats[ivar*(ncat+1)+icat]) for ivar in range(nvars) ]  for icat in range(ncat+1) ]

    print bounds
    
    cuts = []
    cats = []
    catvar = "0"
    prev = None
    for icat in range(ncat):
        cut = ROOT.TCut("1")
        cat = ROOT.TCut("cut%d" % icat)
        if prev:
            cat *= prev
        prev = ROOT.TCut("0")
        for ivar,var in enumerate(varnames):
            cut  = ROOT.TCut( cut.GetTitle() + " && ( %s > %g )" % (var,bounds[icat+1][ivar]) )
            prev = prev.GetTitle() + " || ( %s <= %g )" % (var,bounds[icat+1][ivar])
            
        cuts.append( ("cut%d"%icat,cut) )
        cats.append( ("cat%d"%icat,cat) )
        catvar += "+%d * (cat%d) " % ( icat, icat )

    catvar = ROOT.TCut(catvar)
    selcuts = summary[options.ncat]["selections"]
    selection = ROOT.TCut("cut%d" % (ncat-1) )
    for isel,sel in enumerate(options.selections):
        selection *= ROOT.TCut("%s > %g" % (sel,selcuts[isel]))
    for ivar,var in enumerate(varnames):
        selection *= ROOT.TCut("%s <= %g" % (var,bounds[0][ivar]))

    for name,sel in cuts+cats+[("cat",catvar),("selection",selection)]:
        print name, sel.GetTitle()
        
    tmp = ROOT.TFile.Open("/tmp/musella/tmp.root","recreate")
    for sname,samp in samples.iteritems():
        print "Reading ", sname, samp
        tlist = ROOT.TList()
        for name in samp:
            tree = fin.Get(name)
            tlist.Add(tree)
        tout=ROOT.TTree.MergeTrees(tlist)
        tout.SetName(sname)
        trees[sname] = tout
            
    models = {}
    for name,tree in trees.iteritems():
        for an,ad in cuts+cats:
            tree.SetAlias(an,ad.GetTitle())
        tree.SetAlias("cat",catvar.GetTitle())
        model = ROOT.TH2F("model_%s" % name, "model_%s" % name, nbins, obsmin, obsmax, ncat, 0, ncat )
        tree.Draw("cat:%s>>model_%s" % (obsname,name), ROOT.TCut("_weight") * selection, "goff")
        models[name] = model
        objs.append(model)
        model.Draw()
        
    ### bounds.sort()
    ### ybins = numpy.array(bounds)
    ### xbins = numpy.arange(obsmin,obsmax+binsize,binsize)
    ### for name,tree in trees.iteritems():
    ###     model = ROOT.TH2F("model_%s" % name, "model_%s" % name, len(xbins)-1, xbins, len(ybins)-1, ybins )
    ###     tree.Draw("diphoMVA:mass>>model_%s" % name, "_weight", "goff")
    ###     models[name] = model
    ###     objs.append(model)
    ###     ## model.Draw()

    ws = ROOT.RooWorkspace("cms_hgg","cms_hgg")
    mgg = ws.factory("CMS_hgg_mass[%g,%g]" % (obsmin,obsmax) )
    mgg.setBins(nbins)

    procs = []
    for name,model in models.iteritems():
        if not "bkg" in name:
            procs.append(name)
        for icat in range(ncat):
            slice = model.ProjectionX("%s_cat%d" % (name, icat), icat+1, icat+1 )
            print slice.Integral()
            data = ROOT.RooDataHist(slice.GetName(),slice.GetName(),ROOT.RooArgList(mgg),slice)
            print data.sumEntries()
            getattr(ws,"import")(data)
            if "bkg" in name:
                norm = slice.Integral()
                order = 0
                while norm > poly[order]:
                    if order >= len(poly)-1:
                        break
                    order += 1
                pdf = mkPdf("pol",order+2,icat,ws)
                pdf.fitTo(data)

                
    ws.writeToFile(options.out)

    datacard = open(options.out.replace("root","txt"),"w+")
    datacard.write("""
----------------------------------------------------------------------------------------------------------------------------------
imax * number of bins
jmax * number of processes minus 1
kmax * number of nuisance parameters
----------------------------------------------------------------------------------------------------------------------------------\n""")

    datacard.write("shapes data_obs * %s cms_hgg:bkg_$CHANNEL\n" % options.out)
    datacard.write("shapes bkg *      %s cms_hgg:model_$CHANNEL\n" % options.out)

    for proc in procs:
        datacard.write("shapes %s *   %s cms_hgg:%s_$CHANNEL\n" % (proc,options.out,proc))
    
    datacard.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    datacard.write("bin".ljust(20))
    for icat in range(ncat):
        datacard.write((" cat%d" % icat).ljust(5) )
    datacard.write("\n")

    datacard.write("observation".ljust(20))
    for icat in range(ncat):
        datacard.write(" -1".ljust(5) )
    datacard.write("\n")
        

    datacard.write("----------------------------------------------------------------------------------------------------------------------------------\n")
    
    datacard.write("bin".ljust(20))
    for icat in range(ncat):
        for proc in range(len(procs)+1):
            datacard.write((" cat%d" % icat).ljust(5) )
    datacard.write("\n")


    datacard.write("process".ljust(20))
    for icat in range(ncat):
        for proc in procs:
            datacard.write((" %s" % proc).ljust(5) )
        datacard.write(" bkg".ljust(5) )
    datacard.write("\n")
    
    datacard.write("process".ljust(20))
    for icat in range(ncat):
        for proc in range(len(procs)):
            datacard.write((" %d" % -(proc+1)).ljust(5) )
        datacard.write(" 1".ljust(5) )
    datacard.write("\n")
        
    datacard.write("rate".ljust(20))
    for icat in range(ncat):
        for proc in range(len(procs)):
            datacard.write(" -1".ljust(5) )
        datacard.write(" 1".ljust(5) )
    datacard.write("\n")

    datacard.write("----------------------------------------------------------------------------------------------------------------------------------\n\n")
        
    
if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-i", "--infile",
                        action="store", type="string", dest="file",
                        default="",
                        help="input file",
                        ),
            make_option("-o", "--out",
                        action="store", type="string", dest="out",
                        default="",
                        help="",
                        ),
            make_option("-d", "--cat-def",
                        action="store", type="string", dest="catdef",
                        default="",
                        help="categories definition file",
                        ),
            make_option("-s", "--settings",
                        action="store", type="string", dest="settings",
                        default="",
                        help="json file with additional settings",
                        ),
            make_option("-N", "--nbins",
                        action="store", type="int", dest="nbins",
                        default=320,
                        help="number of categories",
                        ),
            make_option("-n", "--ncat",
                        action="store", type="string", dest="ncat",
                        default="",
                        help="number of categories",
                        ),
            ]
                          )

    (options, args) = parser.parse_args()
    ## sys.argv.append("-b")

    with open(options.settings) as settings:
        options.__dict__.update(json.loads(settings.read()))
    
    pprint(options.__dict__)

    import ROOT
    
    main(options,args)
        
