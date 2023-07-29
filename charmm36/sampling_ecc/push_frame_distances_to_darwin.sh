#!/bin/bash

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do
    cd $pair
    scp *.npy darwin.hpc.udel.edu:/lustre/lenhoff/users/2688/namd/brute_force_tip_scaled/${pair}/
    scp *.txt darwin.hpc.udel.edu:/lustre/lenhoff/users/2688/namd/brute_force_tip_scaled/${pair}/
    cd ../
done

