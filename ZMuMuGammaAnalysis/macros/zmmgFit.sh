#!/bin/bash

mydir=$(dirname $(which $0))

python ${mydir}/zmmgFit.py \
    -g '0,1,2,3' \
    -l 'EBPt40' \
    -g '4,5' \
    -l 'EEPt40' \
    -g '6' -g '7' -g '8,9,14,15' \
    -l 'EBLowEtaHighR9Pt30' -l 'EBLowEtaLowR9Pt30' -l 'EBHighEtaPt25' \
    -g '10' -g '11' \
    -l 'EEHighR9Pt30' -l 'EELowR9Pt30' \
    -g '12' -g '13' \
    -l 'EBLowEtaHighR9Pt25' -l 'EBLowEtaLowR9Pt25'\
    -g '16,22' -g '17,23' \
    -l 'EEHighR9Pt20' -l 'EELowR9Pt20' \
    -g '18' -g '19' -g '20,21' \
    -l 'EBLowEtaHighR9Pt20' -l 'EBLowEtaLowR9Pt20' -l 'EBHighEtaPt20' \
    $@ 

    
##     -p 'deltaEg_data' \
##     -p 'deltaEg_data' \
##     -p 'deltaEg_data'       -p 'deltaEg_data'      -p 'deltaEg_data' \
##     -p 'deltaEg_data' -p 'deltaEg_data' \
##     -p 'deltaEg_data'       -p 'deltaEg_data' \
##     -p 'deltaEg_data' -p 'deltaEg_data' \
##     -p 'deltaEg_data'       -p 'deltaEg_data'      -p 'deltaEg_data' \


## -g '16' -g '17' \
##     -l 'EEHighR9Pt25' -l 'EELowR9Pt25' \
