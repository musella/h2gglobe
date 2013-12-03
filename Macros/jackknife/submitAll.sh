for run in RunABCD; do
    for part in  400 800; do 
	### ./submitJackknife.sh Moriond/CiCvsMassfac/Run$run/delta/partitions_$part
	## ./submitJackknife.sh Moriond/CiCvsMassfac/$run/delta/partitions_$part
	./submitJackknife.sh Moriond/CiCvsSumpt2/$run/delta/partitions_$part/Sumpt2
    done
done

### for part in 100 400; do 
###     ./submitJackknife.sh Moriond/CiCvsICHEP/RunAB/delta/partitions_$part
### done
