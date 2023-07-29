#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    mkdir -p $ion
    cd $ion

    cp ../../c_chemistry/${ion}/starting.pdb .
    cp ../../c_chemistry/${ion}/heavy.pdb .

    cp ../long_range.py .

    echo s/xxx_ion_xxx/${ion}/g > ./prep
    sed -f ./prep ../runme.qs > runme.qs
    rm ./prep

    cd ../ 
done
