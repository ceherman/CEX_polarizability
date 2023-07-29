#!/bin/bash

cp ../a_water_box/final_position_0.pdb ./starting.pdb

for ion in acet esna mso4 guan imim mamm
do
    mkdir -p $ion
    cd $ion
    
    cp ../cavity.py .
    cp ../dcdsubsetfile.py .
    cp ../dcdsubsetreporter.py .

    cp ../pdb_files/${ion}_centered.pdb ./${ion}_centered.pdb
    cp ../pdb_files/${ion}_centered_heavy.pdb ./heavy.pdb

    # cp ~/namd/ion_pairs/cgenff/mqct_for_summit_tip/a_equilibrate/${ion}/positioned_ion.pdb .
    # cp ~/namd/ion_pairs/cgenff/mqct_for_summit_tip/b_chemistry_with_charges/${ion}/zero.pdb .

    echo s/xxx_ion_xxx/${ion}/g > ./prep
    sed -f ./prep ../runme.qs > runme.qs
    rm ./prep

    cd ../
done
