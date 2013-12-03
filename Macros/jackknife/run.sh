#!/bin/bash

export BATCH=
export DISPLAY=""

mydir=$(dirname $(which $0))/
##batchdir=$PWD
batchdir=$mydir

set -x
cd $mydir
eval `scramv1 ru -sh`
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$mydir

workdir=$batchdir

while [[ $1 != "--" ]]; do
    case $1 in
	-workdir)
	workdir=$2;
	shift
	;;
    esac
    shift
done
shift

set -x
job=$(which $1)
shift

cd $workdir

pwd
ls

eval $job $@

