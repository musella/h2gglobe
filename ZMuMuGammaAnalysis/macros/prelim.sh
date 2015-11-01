#!/bin/bash

for f in $@; do 
    dir=$(dirname $f); 
    name=$(basename $f); 
    sed 's%Unpublished%Preliminary%' $dir/$name > $dir/prelim_${name}; 
    convert -format png $dir/prelim_${name} $dir/prelim_$(echo $name | sed 's%eps%png%; s%tmp_%%') ; 
done
