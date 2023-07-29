#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate py2

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do
    cd $pair
    cp ../scale_charges.py .
    python scale_charges.py [AION,CION] 0.75 system.psf
    cd ../
done

conda deactivate
