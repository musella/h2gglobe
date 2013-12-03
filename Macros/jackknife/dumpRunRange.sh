#!/bin/bash

name=$1 && shift
min=$1 && shift
max=$1 && shift
seed=$1 && shift


mkdir -p  Moriond/CiCvsMassfac/$name/{delta,CiC,massfac}

### ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/delta -m $min -M $max --randomSeed=$seed --output2=Moriond/CiC/$name/minitree.root --output1=Moriond/massfac/$name/minitree.root --makeTrees -d 200 -d 400 -d 800 Moriond/massfac/mass_fact_ABCD.txt Moriond/CiC/cic_ABCD_cutbvbf.txt 

### ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/delta  -m $min -M $max --randomSeed=$seed --output2=Moriond/CiC/$name/minitree_test.root --output1=Moriond/massfac/$name/minitree_test.root --makeTrees -d 200 -d 400 -d 800 Moriond/massfac/mass_fact_ABCD_overlap.txt Moriond/CiC/cic_ABCD_cutbvbf_overlap.txt 

### ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/delta -m $min -M $max --randomSeed=$seed -d 100 -d 200 -d 300 -d 400  Moriond/CiC/cic_ABCD_cutbvbf.txt Moriond/massfac/mass_fact_ABCD.txt

## ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/CiC -m $min -M $max --randomSeed=$seed -d 100 -d 200 -d 300 -d 400 Moriond/CiC/cic_ABCD_cutbvbf.txt
 
### ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/massfac -m $min -M $max --randomSeed=$seed -d 100 -d 200 -d 300 -d 400 Moriond/massfac/mass_fact_ABCD.txt

### ./dump2minitree.py --ebOnly -o Moriond/CiCvsMassfac/$name/delta -m $min -M $max --doMigrationMatrix Moriond/CiC/cic_ABCD_cutbvbf.txt Moriond/massfac/mass_fact_ABCD.txt 

./dump2minitree.py -o Moriond/CiCvsMassfac/$name/delta -m $min -M $max --doMigrationMatrix Moriond/CiC/cic_ABCD_cutbvbf_overlap.txt Moriond/massfac/mass_fact_ABCD_overlap.txt 

### mkdir -p Moriond/CiCvsICHEP/$name/delta
### 
### ./dump2minitree.py -o Moriond/CiCvsICHEP/$name/delta -m $min -M $max --randomSeed=$seed -d 100 -d 200 -d 300 -d 400  Moriond/CiC/cic_ABCD_cutbvbf.txt Moriond/ICHEP/MITdump_ICHEP_v2.txt


## mkdir -p  Moriond/CiCvsSumpt2/$name/{delta,CiC,Sumpt2}

### ./dump2minitree.py -o Moriond/CiCvsMassfac/$name/delta -m $min -M $max --randomSeed=$seed --output2=Moriond/CiC/$name/minitree.root --output1=Moriond/Sumpt2/$name/minitree.root --makeTrees -d 200 -d 400 -d 800 Moriond/Sumpt2/eventsList_oldvertex_Total.txt Moriond/CiC/cic_ABCD_cutbvbf.txt 

### ./dump2minitree.py -o Moriond/CiCvsSumpt2/$name/delta -m $min -M $max --randomSeed=$seed  -d 200 -d 400 -d 800 Moriond/Sumpt2/eventsList_oldvertex_Total.txt Moriond/CiC/cic_ABCD_cutbvbf.txt 

## ./dump2minitree.py -o Moriond/CiCvsSumpt2/$name/delta -m $min -M $max --randomSeed=$seed  --doMigrationMatrix Moriond/Sumpt2/eventsList_oldvertex_Total.txt Moriond/CiC/cic_ABCD_cutbvbf.txt