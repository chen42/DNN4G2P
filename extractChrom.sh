#!/bin/bash

## extract genotype for each chromosome 
## the genotype.txt file is downloaded from Scientific Data (doi:10.1038/sdata.2014.11) 

for i in {1..21}; do 
  echo $i
  head -1 genotypes.txt >hschr$i.txt
  grep "Rn34_$i[0-9]\{9\}\s" genotypes.txt >>hschr$i.txt
done 

