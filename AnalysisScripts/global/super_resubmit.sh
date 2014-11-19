

DIR=amarini_diffanalysis_v12_pToMscaled_Syst 

[ "$1" != "" ] && DIR=$1 

echo "### doing DIR=$DIR ###"


LIST=$(./check_fitter.py  $DIR | grep -v '^$' | tr '\n' '@' | sed 's:@[0-9]\+:\n:g' | grep -v done | tr '@' ' ' | tr -s ' '  | grep -v amarini_ | sed 's:^\ jobs\ in\ [^\ ]*\ ::' | sed 's:fail\|run\|status::g'  | tr '\n' ' ' | tr -s ' ' | tr ' ' ',' | sed 's:,$::' | sed 's:^,::'  )

[ "$LIST" == "" ] && exit 0

#echo ./submit_fitter.py -q 8nh -d $DIR -j ${LIST}
# check if it is running

file=/tmp/amarini/$RANDOM
bjobs -w > $file
for job in $(echo $LIST | tr ',' ' '); do
	cat $file | grep -v UNKWN | grep $DIR | grep sub$job 2>&1 >/dev/null || LIST2="${LIST2}$job,"
done

LIST2=$(echo $LIST2 | sed 's/,$//')

#echo $DIR-$LIST2
[ "$LIST2" == "" ] && exit 0
echo ./submit_fitter.py -q 8nh -d $DIR -j ${LIST2}
