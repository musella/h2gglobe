#!/bin/bash

mydir=$(dirname $(which $0))

python $mydir/analyticScaleUnc.py \
    -i $mydir/../../AnalysisScripts/common/energy_scale_errors_material.dat \
    -n $mydir/../../AnalysisScripts/common/energy_scale_corr_errors_material.dat \
    -i $mydir/../../AnalysisScripts/common/energy_scale_errors_fnuf.dat \
    -n $mydir/../../AnalysisScripts/common/energy_scale_corr_errors_fnuf.dat \
    -i $mydir/../../AnalysisScripts/common/jan22rereco_8TeV/energy_scale_errors.dat \
    -n $mydir/../../AnalysisScripts/common/energy_scale_corr_errors.dat \
    $@

