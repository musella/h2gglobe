#!/usr/bin/env python

import sys
import math

def getEffAcc(fname):
    fin=open(fname)
    effAcc = {}
    
    for line in fin.read().split("\n"):
        if "mH=125.0" in line:
            toks = [ t.replace(",","") for t in line.split(" ") if t != "" ]
            cat = int(toks[1])
            ggh = float(toks[4])
            qqh = float(toks[6])
            effAcc[cat] = [ggh,qqh]
    fin.close()
    return effAcc


## vbfcats = [5,6,7]
vbfcats = [8,9]

allTunes = {}

isTunes = False
isJec = False
isJer = False

for file in sys.argv[1:]:
    tune = file.split("/")[-2].split("_")[-1]
    allTunes[tune] = getEffAcc(file)
    if "Tune" in tune:
        isTunes = True
    if "jec" in tune:
        isJec = True
    if "jer" in tune:
        isJer = True

### if isTunes:
###     tunes = set([ t for t in allTunes.keys() if "Tune" in t and "UEOFF" not in t])
###     
###     ratios = {}
###     
###     for tune in tunes:
###         nominal = allTunes[tune]
###         ueoff = allTunes["%sUEOFF" % tune ]
###         
###         totggh = sum( map( lambda x: x[0], nominal.itervalues() ) )
###         totqqh = sum( map( lambda x: x[1], nominal.itervalues() ) )
###     
###         totgghUEOFF = sum( map( lambda x: x[0], ueoff.itervalues() ) )
###         totqqhUEOFF = sum( map( lambda x: x[1], ueoff.itervalues() ) )
###     
###         print tune, "(qqh,qqhUEOFF,ggh,gghUEOFF)"
###         print "exA", totqqh, totqqhUEOFF, totggh, totgghUEOFF
###     
###         ggh = []
###         qqh = []
###         gghMigration = []
###         qqhMigration = []
###         gghVBF = 0
###         qqhVBF = 0
###         gghUEOFF = []
###         qqhUEOFF = []
###         gghUEOFFMigration = []
###         qqhUEOFFMigration = []
###         gghVBFUEOFF = 0
###         qqhVBFUEOFF = 0
###         for cat in vbfcats:
###             ggh.append(nominal[cat][0])
###             gghVBF += ggh[-1]
###             gghMigration.append(gghVBF)
###             qqh.append(nominal[cat][1])
###             qqhVBF += qqh[-1]
###             qqhMigration.append(qqhVBF)
###     
###             gghUEOFF.append(ueoff[cat][0])
###             gghVBFUEOFF += gghUEOFF[-1]
###             gghUEOFFMigration.append(gghVBFUEOFF)
###             qqhUEOFF.append(ueoff[cat][1])
###             qqhVBFUEOFF += qqhUEOFF[-1]
###             qqhUEOFFMigration.append(qqhVBFUEOFF)
###             
###             print "cat%d" % cat, qqh[-1], qqhUEOFF[-1], ggh[-1], gghUEOFF[-1]
###     
###         print "ratio", qqhVBFUEOFF / qqhVBF, gghVBFUEOFF / gghVBF
###         print "doubleRatio", (qqhVBFUEOFF/totqqhUEOFF) / (qqhVBF/totqqh), (gghVBFUEOFF/totgghUEOFF) / (gghVBF/totggh)
###         
###         gghMigrationRatio = []
###         qqhMigrationRatio = []
###         for cat in range(len(vbfcats)-1):
###             gghMigration[cat] /= gghVBF
###             qqhMigration[cat] /= qqhVBF
###             gghUEOFFMigration[cat] /= gghVBFUEOFF
###             qqhUEOFFMigration[cat] /= qqhVBFUEOFF
###     
###             gghMigrationRatio.append(gghMigration[cat]/gghUEOFFMigration[cat])
###             qqhMigrationRatio.append(qqhMigration[cat]/qqhUEOFFMigration[cat])
###             
###             print "migration %d %1.1f%% %1.1f%%" % ( vbfcats[cat], 100.*(1.-gghMigration[cat]/gghUEOFFMigration[cat]), (100.*(1.-qqhMigration[cat]/qqhUEOFFMigration[cat]) ) )
###     
###         qqRatioVBF=qqhVBFUEOFF / qqhVBF
###         ggRatioVBF=gghVBFUEOFF / gghVBF
###         
###         qqDoubleRatioVBF=(qqhVBFUEOFF/totqqhUEOFF) / (qqhVBF/totqqh)
###         ggDoubleRatioVBF=(gghVBFUEOFF/totgghUEOFF) / (gghVBF/totggh)
###     
###         ratios[tune] = [ qqRatioVBF, qqDoubleRatioVBF ] + gghMigrationRatio + [ ggRatioVBF, ggDoubleRatioVBF ] + qqhMigrationRatio
###     
###         print
        
    ### print "uncertainties (ratio, doubleRatio, migration, doubleRatio4, doubleRatio5)"
    ### print "qqh", 
    ### for i in range(8):
    ###     print ("%1.1f%%" % (100.*max( map( lambda x : math.fabs(1.-x[i]), ratios.itervalues() ))) ) ,
    ###     if i == 3:
    ###         print "\nggh",
    ### 
    ### print "\n"
    ### 
    ### print "qqh"
    ### for tune in tunes:
    ###     print tune, 
    ###     for i in range(4):
    ###         print ("%1.1f%%" % (100*math.fabs(1.-ratios[tune][i]) ) ),
    ###     print
    ### print "\n"
    ###     
    ### print "ggh"
    ### for tune in tunes:
    ###     print tune, 
    ###     for i in range(4):
    ###         print ("%1.1f%%" % (100*math.fabs(1.-ratios[tune][i+4]) ) ),
    ###     print
    ### print "\n"


if isTunes:
    tunes = set([ t for t in allTunes.keys() if "Tune" in t and "UEOFF" not in t])
    
    ratios = {}

    qqhRelCentral = [ [] for i in range(len(vbfcats)) ]
    qqhRelPlus = [ [] for i in range(len(vbfcats)) ]
    qqhRelMinus = [ [] for i in range(len(vbfcats)) ]
    qqhMigCentral = [ [] for i in range(len(vbfcats)) ]
    qqhMigPlus = [ [] for i in range(len(vbfcats)) ]
    qqhMigMinus = [ [] for i in range(len(vbfcats)) ]

    gghRelCentral = [ [] for i in range(len(vbfcats)) ]
    gghRelPlus = [ [] for i in range(len(vbfcats)) ]
    gghRelMinus = [ [] for i in range(len(vbfcats)) ]
    gghMigCentral = [ [] for i in range(len(vbfcats)) ]
    gghMigPlus = [ [] for i in range(len(vbfcats)) ]
    gghMigMinus = [ [] for i in range(len(vbfcats)) ]

    nomTune = -1
    
    for tune in tunes:
        if tune == "TuneZ2Star":
            nomTune = len(gghRelCentral[0])
        
        nominal = allTunes[tune]
        ueoff = allTunes["%sUEOFF" % tune ]
        
        totggh = sum( map( lambda x: x[0], nominal.itervalues() ) )
        totqqh = sum( map( lambda x: x[1], nominal.itervalues() ) )

        totueoffggh = sum( map( lambda x: x[0], ueoff.itervalues() ) )
        totueoffqqh = sum( map( lambda x: x[1], ueoff.itervalues() ) )

        ggh = [0]
        qqh = [0]
        ueoffggh = [0]
        ueoffqqh = [0]

        for cat in vbfcats:
            ggh.append(ggh[-1]+nominal[cat][0])
            qqh.append(qqh[-1]+nominal[cat][1])
            ueoffggh.append(ueoffggh[-1]+ueoff[cat][0])
            ueoffqqh.append(ueoffqqh[-1]+ueoff[cat][1])

        ggh.append( totggh )
        qqh.append( totqqh )
        ueoffggh.append( totueoffggh )
        ueoffqqh.append( totueoffqqh )

        print 
        print "===================="
        print "Tune", tune
        print "===================="

        print
        print "Relative yields"
        print "--------------------"
        for icat in range(1,len(ggh)-1):
            print "cat", vbfcats[icat-1]
            gghcent  = ggh[icat] / ggh[-1] 
            vars = [ gghcent, ueoffggh[icat]/ueoffggh[-1] ]
            gghplus = max(vars)
            gghminus = min(vars)
            gghRelCentral[icat-1].append(gghcent)
            gghRelPlus[icat-1].append(gghplus/gghcent)
            gghRelMinus[icat-1].append(gghminus/gghcent)
            print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
            
            qqhcent = qqh[icat] / qqh[-1]
            vars = [ qqhcent, ueoffqqh[icat]/ueoffqqh[-1] ]
            qqhplus = max(vars)
            qqhminus = min(vars)
            qqhRelCentral[icat-1].append(qqhcent)
            qqhRelPlus[icat-1].append(qqhplus/qqhcent)
            qqhRelMinus[icat-1].append(qqhminus/qqhcent)
            print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
            print

        print
        print "Migration"
        print "--------------------"
        for icat in range(1,len(ggh)-1):
            print "cat", vbfcats[icat-1]
            gghcent = ggh[icat] / ggh[icat+1]
            vars = [ gghcent, ueoffggh[icat]/ueoffggh[icat+1] ]
            gghplus = max(vars)
            gghminus = min(vars)
            gghMigCentral[icat-1].append(gghcent/gghcent)
            gghMigPlus[icat-1].append(gghplus/gghcent)
            gghMigMinus[icat-1].append(gghminus/gghcent)
            print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
            
            qqhcent = qqh[icat] / qqh[icat+1]
            vars = [ qqhcent, ueoffqqh[icat]/ueoffqqh[icat+1] ]
            qqhplus = max(vars)
            qqhminus = min(vars)
            qqhMigCentral[icat-1].append(qqhcent/qqhcent)
            qqhMigPlus[icat-1].append(qqhplus/qqhcent)
            qqhMigMinus[icat-1].append(qqhminus/qqhcent)
            print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
            print


    print 
    print "===================="
    print "Tune variations"
    print "===================="
    print
    print "Relative yields"
    print "--------------------"
    for icat in range(len(vbfcats)):
        print "cat", vbfcats[icat]

        gghcent  = gghRelCentral[icat][nomTune]
        gghplus = max(gghRelCentral[icat])
        gghminus = min(gghRelCentral[icat])
        print "ggH (PS): %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
        gghplus = max(gghRelPlus[icat])
        gghminus = min(gghRelMinus[icat])
        print "ggH (UE): %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus-1.), 100.*(gghminus-1.) )
        

        qqhcent  = qqhRelCentral[icat][nomTune]
        qqhplus = max(qqhRelCentral[icat])
        qqhminus = min(qqhRelCentral[icat])
        print "qqH (PS): %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        qqhplus = max(qqhRelPlus[icat])
        qqhminus = min(qqhRelMinus[icat])
        print "qqH (UE): %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus-1.), 100.*(qqhminus-1.) )
        print
        
    print
    print "Migration"
    print "--------------------"
    for icat in range(len(vbfcats)):
        print "cat", vbfcats[icat]

        gghcent  = gghMigCentral[icat][nomTune]
        gghplus = max(gghMigCentral[icat])
        gghminus = min(gghMigCentral[icat])
        print "ggH (PS): %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
        gghplus = max(gghMigPlus[icat])
        gghminus = min(gghMigMinus[icat])
        print "ggH (UE): %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus-1.), 100.*(gghminus-1.) )
 
        qqhcent  = qqhMigCentral[icat][nomTune]
        qqhplus = max(qqhMigCentral[icat])
        qqhminus = min(qqhMigCentral[icat])
        print "qqH (PS): %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        qqhplus = max(qqhMigPlus[icat])
        qqhminus = min(qqhMigMinus[icat])
        print "qqH (UE): %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus-1.), 100.*(qqhminus-1.) )
        print

    
if isJec:
    nominal = allTunes["nominal"]
    up      = allTunes["jecUp"]
    down    = allTunes["jecDown"]

    totggh = sum( map( lambda x: x[0], nominal.itervalues() ) )
    totqqh = sum( map( lambda x: x[1], nominal.itervalues() ) )

    totupggh = sum( map( lambda x: x[0], up.itervalues() ) )
    totupqqh = sum( map( lambda x: x[1], up.itervalues() ) )

    totdownggh = sum( map( lambda x: x[0], down.itervalues() ) )
    totdownqqh = sum( map( lambda x: x[1], down.itervalues() ) )
    
    ggh = [0]
    qqh = [0]
    upggh = [0]
    upqqh = [0]
    downggh = [0]
    downqqh = [0]

    for cat in vbfcats:
        ggh.append(ggh[-1]+nominal[cat][0])
        qqh.append(qqh[-1]+nominal[cat][1])
        upggh.append(upggh[-1]+up[cat][0])
        upqqh.append(upqqh[-1]+up[cat][1])
        downggh.append(downggh[-1]+down[cat][0])
        downqqh.append(downqqh[-1]+down[cat][1])

    ggh.append( totggh )
    qqh.append( totqqh )
    upggh.append( totupggh )
    upqqh.append( totupqqh )
    downggh.append( totdownggh )
    downqqh.append( totdownqqh )

    print 
    print "===================="
    print "JEC"
    print "===================="
    
    print
    print "Relative yields"
    print "--------------------"
    for icat in range(1,len(ggh)-1):
        print "cat", vbfcats[icat-1]
        gghcent  = ggh[icat] / ggh[-1] 
        vars = [ gghcent, upggh[icat]/upggh[-1], downggh[icat]/downggh[-1] ]
        gghplus = max(vars)
        gghminus = min(vars)
        print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
        
        qqhcent = qqh[icat] / qqh[-1]
        vars = [ qqhcent, upqqh[icat]/upqqh[-1], downqqh[icat]/downqqh[-1] ]
        qqhplus = max(vars)
        qqhminus = min(vars)
        print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        print

    print
    print "Migration"
    print "--------------------"
    for icat in range(1,len(ggh)-1):
        print "cat", vbfcats[icat-1]
        gghcent = ggh[icat] / ggh[icat+1]
        vars = [ gghcent, upggh[icat]/upggh[icat+1], downggh[icat]/downggh[icat+1] ]
        gghplus = max(vars)
        gghminus = min(vars)
        print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )

        qqhcent = qqh[icat] / qqh[icat+1]
        vars = [ qqhcent, upqqh[icat]/upqqh[icat+1], downqqh[icat]/downqqh[icat+1] ]
        qqhplus = max(vars)
        qqhminus = min(vars)
        print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        print

if isJer:
    nominal = allTunes["nominal"]
    up      = allTunes["jerUp"]
    down    = allTunes["jerDown"]
    central = allTunes["jerCentral"]

    totggh = sum( map( lambda x: x[0], nominal.itervalues() ) )
    totqqh = sum( map( lambda x: x[1], nominal.itervalues() ) )

    totupggh = sum( map( lambda x: x[0], up.itervalues() ) )
    totupqqh = sum( map( lambda x: x[1], up.itervalues() ) )

    totdownggh = sum( map( lambda x: x[0], down.itervalues() ) )
    totdownqqh = sum( map( lambda x: x[1], down.itervalues() ) )

    totcentralggh = sum( map( lambda x: x[0], central.itervalues() ) )
    totcentralqqh = sum( map( lambda x: x[1], central.itervalues() ) )

    ggh = [0]
    qqh = [0]
    upggh = [0]
    upqqh = [0]
    downggh = [0]
    downqqh = [0]
    centralggh = [0]
    centralqqh = [0]

    for cat in vbfcats:
        ggh.append(ggh[-1]+nominal[cat][0])
        qqh.append(qqh[-1]+nominal[cat][1])
        upggh.append(upggh[-1]+up[cat][0])
        upqqh.append(upqqh[-1]+up[cat][1])
        downggh.append(downggh[-1]+down[cat][0])
        downqqh.append(downqqh[-1]+down[cat][1])
        centralggh.append(centralggh[-1]+central[cat][0])
        centralqqh.append(centralqqh[-1]+central[cat][1])

    ggh.append(totggh)
    qqh.append(totqqh)
    upggh.append(totupggh)
    upqqh.append(totupqqh)
    downggh.append(totdownggh)
    downqqh.append(totdownqqh)
    centralggh.append(totcentralggh)
    centralqqh.append(totcentralqqh)

    vbfcats.append("all")
    
    #### print "Absolute yields"
    #### print "--------------------"
    #### for icat in reversed(range(1,len(ggh))):
    ####     print "cat", vbfcats[icat-1]
    ####     gghcent  = ggh[icat]
    ####     vars = [ gghcent, upggh[icat], downggh[icat], centralggh[icat] ]
    ####     gghplus = max(vars)
    ####     gghminus = min(vars)
    ####     print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
    ####     
    ####     qqhcent = qqh[icat]
    ####     vars = [ qqhcent, upqqh[icat], downqqh[icat], centralqqh[icat] ]
    ####     qqhplus = max(vars)
    ####     qqhminus = min(vars)
    ####     print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
    ####     print

    print 
    print "===================="
    print "JER"
    print "===================="

    print
    print "Relative yields"
    print "--------------------"
    for icat in reversed(range(1,len(ggh)-1)):
        print "cat", vbfcats[icat-1]
        gghcent  = ggh[icat] / ggh[-1] 
        vars = [ gghcent, upggh[icat]/upggh[-1], downggh[icat]/downggh[-1], centralggh[icat]/centralggh[-1] ]
        gghplus = max(vars)
        gghminus = min(vars)
        print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )
        
        qqhcent = qqh[icat] / qqh[-1]
        vars = [ qqhcent, upqqh[icat]/upqqh[-1], downqqh[icat]/downqqh[-1], centralqqh[icat]/centralqqh[-1] ]
        qqhplus = max(vars)
        qqhminus = min(vars)
        print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        print

    print
    print "Migration"
    print "--------------------"
    for icat in reversed(range(1,len(ggh)-1)):
        print "cat", vbfcats[icat-1]
        gghcent = ggh[icat] / ggh[icat+1]
        vars = [ gghcent, upggh[icat]/upggh[icat+1], downggh[icat]/downggh[icat+1], centralggh[icat]/centralggh[icat+1] ]
        gghplus = max(vars)
        gghminus = min(vars)
        print "ggH: %1.2g %1.1f%% %1.1f%%" % ( gghcent, 100.*(gghplus/gghcent-1.), 100.*(gghminus/gghcent-1.) )

        qqhcent = qqh[icat] / qqh[icat+1]
        vars = [ qqhcent, upqqh[icat]/upqqh[icat+1], downqqh[icat]/downqqh[icat+1], centralqqh[icat]/centralqqh[icat+1] ]
        qqhplus = max(vars)
        qqhminus = min(vars)
        print "qqH: %1.2g %1.1f%% %1.1f%%" % ( qqhcent, 100.*(qqhplus/qqhcent-1.), 100.*(qqhminus/qqhcent-1.) )
        print
