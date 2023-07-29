#!/bin/bash

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do
    rsync -avz darwin.hpc.udel.edu:/lustre/lenhoff/users/2688/ion_pairs/${pair}/pair_data/pairwise_ener_and_dist_head.csv ./${pair}/pair_data/pairwise_ener_and_dist_head.csv
done
