#!/bin/bash

for cation in acet esna mso4
do
    for anion in guan mamm imim
    do
        mkdir -p ${cation}_${anion}
        cd ${cation}_${anion}
        cp /home/chase/namd/ion_pairs/cgenff/shared/pdb_files/${cation}.pdb .
        cp /home/chase/namd/ion_pairs/cgenff/shared/pdb_files/${anion}.pdb .
        cp /home/chase/namd/ion_pairs/cgenff/shared/pdb_files/tip3.pdb .
        cp ../starting.xsc .
        cd ..
    done
done
