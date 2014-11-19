import os,sys
from optparse import OptionParser
from glob import glob
import re

DEBUG=0

parser = OptionParser()
parser.add_option("-d","--dir",dest="dir",help="Directory to parse")
parser.add_option("-e","--exclude",dest="exclude",help="Exclude Regexp",default="")
parser.add_option("-i","--include",help="Include Regexp",default="")
parser.add_option("-o","--output",help="OutputFile. Default=%default",default="MH_Scan.pdf")
#parser.add_option("-s","--substitute",help="substitute regexp for title. comma separated.",default="")
parser.add_option("-s","--substitute",action='append',help="substitute regexp for title. comma separated.",default=[])
parser.add_option("-b","--batch",dest="batch",help="Batch",action='store_true',default=False)
parser.add_option("","--lowMH",dest="lowMH",help="lowMH value. Default=%default",type='float',default=123.)
parser.add_option("","--highMH",dest="highMH",help="highMH value. Default=%default",type='float',default=127.)

(opts,args)=parser.parse_args()
#opts.substitute.reverse()


sys.argv=[]
if opts.batch: sys.argv.append("-b")
import ROOT
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
if opts.batch: ROOT.gROOT.SetBatch()

listOfDir=glob("%s/*"%opts.dir)

listOfTree=[]
obj=[] ## no garbage collector on these objects

c=ROOT.TCanvas("c","c")
legend=ROOT.TLegend(0.30,.5,.70,.89)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

dummy=ROOT.TH2D("dummy",";M_{H}[GeV];#DeltaNLL",100,opts.lowMH,opts.highMH,100,0,2.5)
dummy.Draw("")

line=ROOT.TGraph()
line.SetName("line")
line.SetPoint(0,100,0.5)
line.SetPoint(1,150,0.5)
line.Draw("L SAME")

line2=ROOT.TGraph()
line2.SetName("line2")
line2.SetLineColor(ROOT.kGray)
line2.SetPoint(0,100,2.)
line2.SetPoint(1,150,2.)
line2.Draw("L SAME")

drawopts="C SAME"
colors=[ROOT.kRed,ROOT.kBlack,ROOT.kGreen+2,ROOT.kOrange,ROOT.kBlue-4,ROOT.kMagenta+2,ROOT.kCyan,ROOT.kGray]
markers=[7,20,22,23,27]
linestyles=[0,7]

colors.reverse()
markers.reverse()
for dir in listOfDir:
	if DEBUG: print "DEBUG: Considering dir",dir
	if opts.exclude != "" and re.search(opts.exclude,dir): continue
	if DEBUG: print "DEBUG: -- pass exclude regexp",opts.exclude
	if opts.include != "" and not re.search(opts.include,dir): continue
	if DEBUG: print "DEBUG: -- pass include regexp",opts.include

	if dir[-1] =='/': dir=dir[:-1]
	dirName=re.sub('.*/','',dir)
	fileName=dir+ "/" + dirName + ".root"

	if DEBUG: print "DEBUG: -- fileName=",fileName
	f=ROOT.TFile.Open(fileName)

	tree=f.Get("limit")

	if tree == None:  print "tree in",fileName,"does not exist"

	listOfTree.append(tree)
	
	#if len(color)>0:
	#	tree.SetMarkerColor(color.pop())

	if 'Unfold' in dir:
		color=colors.pop()
		colors=[color] + colors
	else:
		color=colors[0]

	tree.SetMarkerColor(color)
	tree.SetLineColor(color)

	marker=markers.pop()	
	markers=[marker] + markers
	#tree.SetMarkerStyle(marker)

	#tree.Draw("deltaNLL:MH>>%s"%dirName,"",drawopts)
	tree.Draw("deltaNLL:MH>>th2_%s"%dirName,"","goff")
	#  Root > TGraph *gr = new TGraph(ntuple->GetSelectedRows(),
	#		                                     ntuple->GetV2(), ntuple->GetV1());

	graph=ROOT.TGraph(tree.GetSelectedRows(),tree.GetV2(),tree.GetV1())
	graph.SetName(dirName)


	#graph=ROOT.gDirectory.Get(dirName)
	graph.Sort()

	style=linestyles.pop()
	linestyles= [style] + linestyles
	graph.SetLineColor(color)
	graph.SetLineStyle(style)
	graph.SetLineWidth(2)
	obj.append(graph)

	graph.Draw(drawopts)

	if "SAME" not in drawopts: drawopts+= " SAME"

	graphTitle=dirName
	for substr in opts.substitute:
		if DEBUG: print "DEBUG: -- -- SubString=",substr
		graphTitle=re.sub(substr.split(',')[0],substr.split(',')[1],graphTitle)
	legend.AddEntry(graph,graphTitle,"L")


legend.Draw()
dummy.Draw("AXIS SAME")
dummy.Draw("AXIS X+ Y+SAME")
#c.SaveAs("MH_Scan.pdf")
c.SaveAs(opts.output)
if 'pdf' in opts.output or 'png' in opts.output: c.SaveAs(opts.output.replace('pdf','root'))

