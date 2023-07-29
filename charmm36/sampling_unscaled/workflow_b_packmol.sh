#!/bin/bash

for cation in acet esna mso4
do
    for anion in guan mamm imim
    do
        cd ${cation}_${anion}
        echo s/XXX_cation_XXX/${cation}/g > tmp
        echo s/XXX_anion_XXX/${anion}/g >> tmp
        sed -f ./tmp ../packmol_template.inp > packmol.inp
        rm tmp
        packmol < packmol.inp > packmol.log
        cd ..
    done
done
