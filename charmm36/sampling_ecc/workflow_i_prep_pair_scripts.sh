#!/bin/bash

declare -A abbrev
abbrev=( ["acet"]="Ac" ["esna"]="Es" ["mso4"]="Ms" ["guan"]="Gu" ["imim"]="Im" ["mamm"]="Ma" )

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
        for i_anion in {1..22}
        do
            name=${abbrev[$anion]}${abbrev[$cation]}${i_anion}
            pair=${anion}_${cation}
            echo s/xxx_name_xxx/${name}/g > ./tmp
            echo s/xxx_pair_xxx/${pair}/g >> ./tmp
            echo s/xxx_i_anion_xxx/${i_anion}/g >> ./tmp
            sed -f ./tmp ./template_job_get_energies.qs > job_get_energies_${anion}_${cation}_${i_anion}.qs
            rm ./tmp
        done
    done
done

