#!/bin/bash

dir=$1 && shift

for d in $(find $dir -type d -name part[0-9]*); do
	rm $d/batch.log
	bsub -q 1nh -o $d/batch.log run.sh -- ./doBestMuJackknife.sh $d datacard.txt BestMu
done
