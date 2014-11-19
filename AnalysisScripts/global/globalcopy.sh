#!/bin/bash
[ -f globaloptions.sh ] && source globaloptions.sh
[ -f global/globaloptions.sh ] && source global/globaloptions.sh

for dir in ${USER}_$LABEL* ; 
  do 
	  FILE2=$( echo "CMS-HGG_`echo $dir | sed "s/${USER}_//"`_*.root" )
	  FILE=$( echo $FILE2 )
	  [ -f "${FILE}" ] && 
	  	{ echo "file ${FILE} already exist" ; } || 
		{ cp -v  $dir/CMS-HGG.root CMS-HGG_`echo $dir | sed "s/${USER}_//"`_$(date +%Y_%m_%d).root  ; }
  done

###### END ##### 
