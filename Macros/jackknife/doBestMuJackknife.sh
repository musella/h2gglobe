#!/bin/bash

set -x

parallel=$(dirname $(which $0))/parallel
blindScript=$(dirname $(which $0))/blindLimitTree.py

wd=$1 && shift
datacard=$1 && shift
label=$1 && shift

min=120
max=130
step=5

[[ -n $1 ]] && min=$1 && shift 
[[ -n $1 ]] && max=$1 && shift 
[[ -n $1 ]] && step=$1 && shift 

njobs=1
if ( hostname | grep lxplus ); then njobs=8; fi

cd $wd
mkdir $label 

rm higgsCombine$label.MaxLikelihoodFit.mH*.root

seq $min $step $max | $parallel -j $njobs "combine -M MaxLikelihoodFit --verbose=2 --rMin=-10. --rMax=10. -n $label -m {} -S 1 $datacard | grep -A 1 'Fit failed'"

hadd -f $label/higgsCombine$label.MaxLikelihoodFit.root higgsCombine$label.MaxLikelihoodFit.mH*.root 

$blindScript -s $(cat seed.txt) $label/higgsCombine$label.MaxLikelihoodFit.root $label/higgsCombine$label.MaxLikelihoodFit_blind.root

rm higgsCombine$label.MaxLikelihoodFit.mH*.root


