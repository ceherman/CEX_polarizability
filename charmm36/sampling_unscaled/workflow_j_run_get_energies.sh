#!/bin/bash

for i_min in 1 4 7 10 13 16 19
do
    for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
    do
        sbatch job_get_energies_${pair}_${i_min}.qs
    done
done



