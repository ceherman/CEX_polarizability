#!/bin/bash
# Get files for equilibrating systems

for ion in acet esna mso4 guan imim mamm
do
    cd $ion
    
    bsub run_equil.lsf

    cd ../
done
