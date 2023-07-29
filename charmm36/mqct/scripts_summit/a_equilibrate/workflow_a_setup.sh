#!/bin/bash

for ion in acet esna mso4 guan mamm imim
do 
    mkdir -p ${ion}
    cd ${ion}
    cp /home/chase/namd/ion_pairs/cgenff/shared/pdb_files/${ion}.pdb ./ion.pdb
    cp /home/chase/namd/ion_pairs/cgenff/shared/pdb_files/tip3.pdb .
    cp ../files/starting.xsc ../files/packmol.inp
    cd ..
done
