#!/bin/bash
# To be run locally
# Python 3 and 2

eval "$(conda shell.bash hook)"

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    python process_seven_point_openmm.py

    conda activate py2
    python 7p_integral.py force.dat > integral.dat
    conda deactivate

    cd ../
done
