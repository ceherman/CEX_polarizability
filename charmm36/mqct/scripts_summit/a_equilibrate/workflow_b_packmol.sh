#!/bin/bash
# Get files for equilibrating systems

for ion in acet esna mso4 guan imim mamm
do
    cd $ion
    packmol < packmol.inp > packmol.log
    cd ../
done


