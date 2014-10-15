#!/bin/bash

mydir=$(dirname $(which $0))

### python ${mydir}/zmmgScale.py $1 -o $2/split_ebee   \
###     -g "0,1,4,5,8,9" -l "EB" -g "2,3,6,7,10,11" -l "EE"
### 
### python ${mydir}/zmmgScale.py $1 -o $2/split_hilopt \
###     -g "0,1" -l "EBHighPt" -g "4,5" -l "EBMidPt" -g "8,9" -l "EBLowPt" \
###     -g "2,3" -l "EEHighPt" -g "6,7" -l "EEMidPt" -g "10,11" -l "EELowPt" 
### 
### python ${mydir}/zmmgScale.py $1 -o $2/split_hilor9 \
###     -g "0,4,8" -l "EBHighR9" -g "1,5,9" -l "EBLowR9" \
###     -g "2,6,10" -l "EEHighR9" -g "3,7,11" -l "EELowR9" 
### 
### python ${mydir}/zmmgScale.py $1 -o $2/split_all \
###     -l 'EBHighR9HighPt' -l 'EBLowR9HighPt' \
###     -l 'EEHighR9HighPt' -l 'EELowR9HighPt' \
###     -l 'EBHighR9MidPt'  -l 'EBLowR9MidPt' \
###     -l 'EEHighR9MidPt'  -l 'EELowR9MidPt' \
###     -l 'EBHighR9LowPt'  -l 'EBLowR9LowPt' \
###     -l 'EEHighR9LowPt'  -l 'EELowR9LowPt' 
    
python ${mydir}/zmmgScale.py $1 -o $2 \
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
    -l 'EEHighR9Pt25' -l 'EELowR9Pt25' \
    -g '18' -g '19' -g '20,21' \
    -l 'EBLowEtaHighR9Pt20' -l 'EBLowEtaLowR9Pt20' -l 'EBHighEtaPt20'
    