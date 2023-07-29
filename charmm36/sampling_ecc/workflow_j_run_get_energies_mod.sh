#!/bin/bash

for pair in mso4_mamm # mso4_imim # acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan # mso4_imim mso4_mamm
do
    for i_anion in {1..22}
    do
        sbatch job_get_energies_${pair}_${i_anion}.qs
    done
done

