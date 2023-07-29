#!/bin/bash
# Python 3

path=/home/chase/namd/ion_pairs/cgenff/mqct_for_summit_tip/c_charging_conditioned

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    cp ${path}/${ion}/just_solutes.pdb .
    cp ${path}/${ion}/just_solutes.psf .

    ln -sf ../self_clean_local.py .
    ln -sf ../get_box_length_average.py .
    python get_box_length_average.py

    cd ../
done
