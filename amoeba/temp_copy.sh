#!/bin/bash

rm -r sampling
mkdir sampling
cd sampling
cp /home/chase/namd/openmm/ion_pairs/* .

for aion in acet esna mso4
do
    for cion in guan imim mamm
    do
        mkdir ${aion}_${cion}
        rsync -r --exclude '*.chk' --exclude '*.npy' --exclude 'pairwise_ener_and_dist_head.csv' --exclude 'prev_wrong_pairwise_ener_means_pme_off.csv' --exclude '*.log' --exclude '*.dcd' /home/chase/namd/openmm/ion_pairs/${aion}_${cion} .
    done
done

cd ../
