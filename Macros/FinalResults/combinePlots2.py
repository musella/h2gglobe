#!/usr/bin/python
import os,sys
import array
from glob import glob
from subprocess import call
from optparse import OptionParser

##### CONFIGURATION ######
nBins_=6 # later figured out
mass_=125
sigma_=1
wsFile_="CMS-HGG.root"
###      red green, blue, orange,cyan, yelow
colors_=[632,416,600,800,432,400+2,416+2,632+2,58]
dir_='jobs'
Lumi=19.7
##########################

############ PARSER 
if __name__=="__main__":
	usage = "usage: %prog [options]"
	parser=OptionParser(usage=usage)
	parser.add_option("-b","--batch" ,dest='batch',action='store_true',help="Batch Mode. Default=%default",default=False)
	parser.add_option("-D","--dir" ,dest='dir',type='string',help="Directory. Default=%default",default=dir_)
	parser.add_option("-s","" ,dest='sig',type='string',help="Ws Sig not fitted. Default=%default",default=wsFile_)
	parser.add_option("-v","--var" ,dest='var',type='string',help="Variable. If non null read bins from the var file. Default=%default",default="")
	parser.add_option("-k","--split" ,dest='split',action='store_true',help="Add split info for root files for Nicolas (>v5). Default=%default",default=True)
	parser.add_option("-K","--nosplit" ,dest='split',action='store_false',help="Dont split info for root files.")
	parser.add_option("","--unblind" ,dest='unblind',action='store_true',help="Unblind Plots. Default=%default",default=False)
	(options,args)=parser.parse_args()
	dir_=options.dir
        wsFile_=options.sig

print "Importing ROOT"
sys.argv=[]
import ROOT
if options.batch: ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine(
		'struct entry{\
		Float_t var;\
		Float_t nll;\
		};'
		)
from ROOT import entry

ROOT.gROOT.ProcessLine("Float_t histBins[100];");
from ROOT import histBins;
import math
from glob import glob



from PlotsLibrary import findPath,getMu,DrawNLL,GetXsec
(mypath,globe_name)=findPath()

#from globe_name.Macros.FinalResults.combineHarvester import getVariableBins 
sys.path.append(mypath+"/Macros/FinalResults")
from combineHarvester import getVariableBins,getVariableBinsFromWs

#take from the file
if options.var == "":
	nBins_=6
	histBins[0]=0
	histBins[1]=20
	histBins[2]=35
	histBins[3]=60
	histBins[4]=130
	histBins[5]=400
else:
	(nBins_,boundaries,jooa)=getVariableBinsFromWs(options.var,wsFile_,verbose=True)
	#(nBins_,boundaries,jooa) = getVariableBins(options.var,verbose=True)
	#nBins_ += 1
	for iBin in range(0,len(boundaries)):
		histBins[iBin] = boundaries[iBin]



## Draw Canvas nll##

ExpStr="Exp"
if options.unblind: ExpStr=""
try:	DrawNLL(dir_,nBins_,"UnfoldScan%s"%ExpStr)
except ReferenceError: pass ## no file
try:	DrawNLL(dir_,nBins_,"RecoScan%s"%ExpStr)
except ReferenceError: pass ## no file
try:	DrawNLL(dir_,nBins_,"RecoScanStat%s"%ExpStr)
except ReferenceError: pass ## no file
try:	DrawNLL(dir_,nBins_,"UnfoldScanStat%s"%ExpStr)
except ReferenceError: pass ## no file

### Get The Histograms  and normalize to the total xSec

# load combine
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
f=ROOT.TFile.Open(wsFile_)
ws=f.Get("cms_hgg_workspace")

xSecPerBin=GetXsec(ws,mass_,nBins_,Lumi)
if options.split:
	xSecSplit={}
	HSplit={}
	procs=["ggh","vbf","wh","zh","tth"]
	for p in procs:
		xSecSplit[p]=GetXsec(ws,mass_,nBins_,Lumi,"_"+p)
		HSplit[p]=ROOT.TH1F("HExp_"+p,"HExpected "+p,nBins_,histBins)

C2=ROOT.TCanvas("c2","c2")
# this are the ones put in the root file
if options.unblind:(Mu,Graphs) = getMu(nBins_,dir_,'UnfoldScan')
else: (Mu,Graphs) = getMu(nBins_,dir_,'UnfoldScanExp')

ROOT.gStyle.SetErrorX(0)
ROOT.gStyle.SetOptStat(0)
H=ROOT.TH1F("data","Data",nBins_,histBins);
HErr=ROOT.TH1F("error","Error",nBins_,histBins);
HExp=ROOT.TH1F("Expected","Expected",nBins_,histBins);

max_h=-1
min_h=0

for iBin in range(0,nBins_):
	print "Mu ",Mu[iBin][0], "+-", Mu[iBin][1],Mu[iBin][2]
	HExp.SetBinContent( iBin+1, xSecPerBin[iBin]/H.GetBinWidth(iBin+1) )
	if options.split:
		for p in procs:
			HSplit[p].SetBinContent(iBin+1, xSecSplit[p][iBin]/H.GetBinWidth(iBin+1))

	low =xSecPerBin[iBin]/H.GetBinWidth(iBin+1) *Mu[iBin][1]
	high=xSecPerBin[iBin]/H.GetBinWidth(iBin+1) *Mu[iBin][2]
	HErr.SetBinContent(iBin+1, (low+high)/2)
	HErr.SetBinError(iBin+1,math.fabs(low-high)/2)
	H.SetBinContent(iBin+1,xSecPerBin[iBin]/H.GetBinWidth(iBin+1) * Mu[iBin][0] )

	max_h=max(max_h,high)
	max_h=max(max_h,low)
	max_h=max(max_h,HExp.GetMaximum())
	min_h=min(min_h,low)
	min_h=min(min_h,high)
	min_h=min(min_h,HExp.GetMinimum())

H.SetMarkerStyle(20)
max_h *= 1.25
min_h *= 1.25  ### <=0
H.SetMaximum(max_h)
H.SetMinimum(min_h)
H.Draw("P")

H.GetYaxis().SetTitle("d#sigma/dP_{T}")
if   options.var=='pToMscaled': 
	H.GetYaxis().SetTitle("d#sigma/dp_{T}")
	H.GetXaxis().SetTitle("p_{T}")
elif options.var=='dPhi': 
	H.GetYaxis().SetTitle("d#sigma/d#phi^{#gamma#gamma}")
	H.GetXaxis().SetTitle("#phi^{#gamma#gamma}")
elif options.var=='Ygg': 
	H.GetYaxis().SetTitle("d#sigma/dy^{#gamma#gamma}")
	H.GetXaxis().SetTitle("y^{#gamma#gamma}")
elif options.var=='Njets': 
	H.GetYaxis().SetTitle("d#sigma/dN_{jets}")
	H.GetXaxis().SetTitle("N_{jets}")
elif options.var=='CosThetaStar': 
	H.GetYaxis().SetTitle("d#sigma/dCos(#theta^{*})")
	H.GetXaxis().SetTitle("Cos(#theta^{*})")
elif options.var=='Fiducial': 
	H.GetYaxis().SetTitle("#sigma")
	H.GetXaxis().SetTitle("")
elif options.var=='LeadJetpT': 
	H.GetYaxis().SetTitle("d#sigma/dp_{T}^{j}")
	H.GetXaxis().SetTitle("p_{T}^{j}")
elif options.var=='dRapidityHiggsJet': 
	H.GetYaxis().SetTitle("d#sigma/dy^{Hj}")
	H.GetXaxis().SetTitle("y^{Hj}")
elif options.var=='MjjExtended': 
	H.GetYaxis().SetTitle("d#sigma/dm^{jj}")
	H.GetXaxis().SetTitle("m^{jj}")
elif options.var=='ZeppExtended': 
	H.GetYaxis().SetTitle("d#sigma/dZepp")
	H.GetXaxis().SetTitle("Zepp")
elif options.var=='dEtajjExtended': 
	H.GetYaxis().SetTitle("d#sigma/d#eta^{jj}")
	H.GetXaxis().SetTitle("#eta^{jj}")
elif options.var=='dPhijjExtended': 
	H.GetYaxis().SetTitle("d#sigma/d#phi^{jj}")
	H.GetXaxis().SetTitle("#phi^{jj}")
elif options.var=='dPhiggjjExtended': 
	H.GetYaxis().SetTitle("d#sigma/d#phi^{H,gg}")
	H.GetXaxis().SetTitle("#phi^{H,jj}")


HExp.SetLineColor(ROOT.kRed)
HExp.SetLineWidth(2)
HExp.Draw("HIST SAME")
HErr.Draw("P E SAME")
H.Draw("P SAME")

C2.SaveAs("xSec_"+dir_.replace("/","")+".pdf")
C2.SaveAs("xSec_"+dir_.replace("/","")+".png")
C2.SaveAs("xSec_"+dir_.replace("/","")+".root") #will be deleted by the next line if split
f=ROOT.TFile("xSec_"+dir_.replace("/","")+".root","UPDATE")
f.cd()
H.Write()
HExp.Write()
HErr.Write()
if options.split:
	for p in procs:
		HSplit[p].Write()
f.Close()
	


C3=ROOT.TCanvas("c3","c3",800,800)

try: 	MuU=getMu(nBins_,dir_,"UnfoldScan%s"%ExpStr,1)[0]
except: MuU=None
try:	MuUS=getMu(nBins_,dir_,"UnfoldScanStat%s"%ExpStr,1)[0]
except: MuUS=None
try:	MuR=getMu(nBins_,dir_,"RecoScan%s"%ExpStr,1)[0]
except: MuR=None
try:	MuRS=getMu(nBins_,dir_,"RecoScanStat%s"%ExpStr,1)[0]
except: MuRS=None


max_mu=3
min_mu=-1


for iBin in range(0,nBins_):
	mu=MuU[iBin][0]
	max_mu=max(mu*1.1,max_mu)
	min_mu=min(mu*1.1,min_mu)
	mu=MuR[iBin][0]
	max_mu=max(mu*1.1,max_mu)
	min_mu=min(mu*1.1,min_mu)

h=ROOT.TH2D("axis","axis",nBins_,0,nBins_,100,min_mu,max_mu)
h.GetYaxis().SetTitle("#mu")
h_MuU =ROOT.TGraphAsymmErrors()
h_MuU.SetName("muU")
h_MuUS=ROOT.TGraphAsymmErrors()
h_MuUS.SetName("muUS")
h_MuR =ROOT.TGraphAsymmErrors()
h_MuR.SetName("muR")
h_MuRS=ROOT.TGraphAsymmErrors()
h_MuRS.SetName("muRS")


xerr=0.1
for iBin in range(0,nBins_):
	h.GetXaxis().SetBinLabel(iBin+1,"Bin%d"%iBin)
	if MuU:
		h_MuU.SetPoint(iBin,iBin+0.35, MuU[iBin][0])
		h_MuU.SetPointError(iBin,xerr,xerr ,MuU[iBin][0]- MuU[iBin][1]  ,MuU[iBin][2] - MuU[iBin][0])
	if MuUS:
		h_MuUS.SetPoint(iBin,iBin+0.35, MuUS[iBin][0])
		h_MuUS.SetPointError(iBin,xerr*.9,xerr*.9 ,MuUS[iBin][0]- MuUS[iBin][1], MuUS[iBin][2] - MuUS[iBin][0])
	if MuR:
		h_MuR.SetPoint(iBin,iBin+0.65, MuR[iBin][0])
		h_MuR.SetPointError(iBin,xerr, xerr,MuR[iBin][0]- MuR[iBin][1]  , MuR[iBin][2] - MuR[iBin][0])
	if MuRS:
		h_MuRS.SetPoint(iBin,iBin+0.65, MuRS[iBin][0])
		h_MuRS.SetPointError(iBin,xerr*.9, xerr *.9,MuRS[iBin][0]- MuRS[iBin][1], MuRS[iBin][2] - MuRS[iBin][0])

MuFile =open("Mu_"+dir_.replace("/","")+".txt","w")

print >>MuFile,"\\begin{table}[bp]"
print >>MuFile,"\\centering"
print >>MuFile,"\\begin{tabular}{|c|c|c|c|}"
print >>MuFile,"\\hline"
print >>MuFile,"\\textbf{Bin Number} & \\textbf{$\\mu$} & \\textbf{Negative error} & \\textbf{positive error} \\\\"
print >>MuFile,"\\hline"
if MuU:
   for iBin in range(0,nBins_):
	print "Mu Bin%d"%iBin,MuU[iBin][0], "+-", MuU[iBin][1],MuU[iBin][2]
	print>>MuFile, "Bin%d"%iBin,"& $",MuU[iBin][0], "$ & $", MuU[iBin][0]-MuU[iBin][1],"$ & $",MuU[iBin][2] - MuU[iBin][0],"$ \\\\"
print >>MuFile,"\\hline"
print >>MuFile,"\\end{tabular}"
if options.unblind: 	print >>MuFile,"\\caption{Observed signal-strength stat+syst for %s.}"%options.var
else : 			print >>MuFile,"\\caption{Expected signal-strength stat+syst for %s.}"%options.var
print >>MuFile,"\\end{table}"
print >>MuFile

print >>MuFile,"%%%%%%%%%%%%%%% STAT ONLY %%%%%%%%%%%%%%%%%%"
print >>MuFile,"%%\\begin{table}[bp]"
print >>MuFile,"%%\\centering"
print >>MuFile,"%%\\begin{tabular}{|c|c|c|c|}"
print >>MuFile,"%%\\hline"
print >>MuFile,"%%\\textbf{Bin Number} & \\textbf{$\\mu$} & \\textbf{Negative error} & \\textbf{positive error} \\\\"
print >>MuFile,"%%\\hline"
if MuUS:
   for iBin in range(0,nBins_):
	print>>MuFile, "%%%%Bin%d"%iBin,"& $",MuUS[iBin][0], "$ & $", MuUS[iBin][0]-MuUS[iBin][1],"$ & $",MuUS[iBin][2] - MuUS[iBin][0],"$ \\\\"
print >>MuFile,"%%\\hline"
print >>MuFile,"%%\\end{tabular}"
if options.unblind:	print >>MuFile,"%%%%\\caption{Observed signal-strength stat-only for %s.}"%(options.var)
else:			print >>MuFile,"%%%%\\caption{Expected signal-strength stat-only for %s.}"%(options.var)
print >>MuFile,"%%\\end{table}"

print >>MuFile
#Style

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

h_MuU.SetMarkerStyle(20)
h_MuU.SetFillColor(ROOT.kBlue - 4)

h_MuUS.SetMarkerStyle(20)
h_MuUS.SetFillColor(38)

h_MuR.SetMarkerStyle(20)
h_MuR.SetFillColor(ROOT.kRed - 7)

h_MuRS.SetMarkerStyle(20)
h_MuRS.SetFillColor(46)

h.Draw("AXIS")
h.Draw("AXIS Y+ X+ SAME")

h_MuU.Draw("E2 SAME")
h_MuR.Draw("E2 SAME")
h_MuUS.Draw("E2 SAME")
h_MuRS.Draw("E2 SAME")

#redraw P on top X=no error
h_MuU.Draw("P X SAME")
h_MuR.Draw("P X SAME")


C3.SaveAs("Mu_"+dir_.replace("/","")+".pdf")
C3.SaveAs("Mu_"+dir_.replace("/","")+".png")
C3.SaveAs("Mu_"+dir_.replace("/","")+".root")
