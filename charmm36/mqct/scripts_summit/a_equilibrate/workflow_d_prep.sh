#!/bin/bash
# Get files for equilibrating systems

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    cp ../files/equilibrate.namd .
    
    echo s/xxx_ion_xxx/${ion}/g > ./prep
    sed -f ./prep ../files/run_equil.lsf > run_equil.lsf
    rm ./prep
    
    cd ../
done
