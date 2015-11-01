#!/bin/bash

mydir=$(dirname $(which $0))

python -i ${mydir}/zmmgBins.py \
    -g '0,1,2,3' \
    -g '4,5' \
    -g '6' -g '7' -g '8,9,14,15' \
    -g '10' -g '11' \
    -g '12' -g '13' \
    -g '16,22' -g '17,23' \
    -g '18' -g '19' -g '20,21' \
    $@ 
