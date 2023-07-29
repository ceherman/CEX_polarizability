#!/bin/bash

for pair in acet_imim acet_mamm esna_guan esna_imim
do
    for i_anion in {1..22}
    do
        sbatch job_get_energies_2_${pair}_${i_anion}.qs
    done
done

