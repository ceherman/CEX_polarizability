#!/bin/bash

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do
    mkdir -p ${pair}/pair_data_charmm
    # mv ./${pair}/pair_data_charmm/pairwise_ener_means_pme_off.csv ./${pair}/pair_data_charmm/prev_wrong_pairwise_ener_means_pme_off.csv

    scp -r darwin.hpc.udel.edu:/lustre/lenhoff/users/2688/ion_pairs/${pair}/pair_data_charmm/pairwise_ener_means_pme_off.csv ./${pair}/pair_data_charmm/pairwise_ener_means_pme_off.csv
done
