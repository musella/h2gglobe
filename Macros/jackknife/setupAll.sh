for run in RunABCD; do
    for part in 200 400 800; do 
	## ./setupJackknife.sh Moriond/CiC/Run$run/ Moriond/massfac/Run$run/ Moriond/CiCvsMassfac/Run$run/delta/partitions_$part.json
	## ./setupJackknife.sh Moriond/CiC/$run/ Moriond/massfac/$run/ Moriond/CiCvsMassfac/$run/delta/partitions_$part.json
	./setupJackknife.sh Moriond/CiC/$run/ Moriond/Sumpt2/$run/ Moriond/CiCvsSumpt2/$run/delta/partitions_$part.json
    done
done

## for part in 100 400; do 
##     ./setupJackknife.sh Moriond/CiC/RunAB/ Moriond/ICHEP/RunAB/ Moriond/CiCvsICHEP/RunAB/delta/partitions_$part.json
## done
