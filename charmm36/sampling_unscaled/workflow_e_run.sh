#!/bin/bash

i=0

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do 
    cd $pair
    sbatch job_${i}.qs
    cd ../
done
