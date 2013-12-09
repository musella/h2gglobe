#!/bin/bash

export DISPLAY=""

dir=$1

### for f in $(find  $dir -name CMS-HGG\*.root); do
###     d=$(dirname $f)    
###     yes | python ../Macros/makeEffAcc.py $f | tee $d/effAcc.txt
### done

for f in $(find -L $dir -name effAcc.txt); do
    echo 
    echo 
    grep -H '^cat [56789]' $f | sed 's%.effAcc.txt%%; s% [ ]*%,%g' | tail -5
done | tee $dir/summary.csv

