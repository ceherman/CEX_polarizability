#!/bin/bash

for i_min in 1 4 7 10 13 16 19
do
    if [[ $i_min -eq 19 ]]
    then
        i_max=22
    else
        let i_max=$i_min+2
    fi

    declare -A names
    names=( ["acet_guan"]="AcGu$i_min" ["acet_imim"]="AcIm$i_min" ["acet_mamm"]="AcMa$i_min" ["esna_guan"]="EsGu$i_min" ["esna_imim"]="EsIm$i_min" ["esna_mamm"]="EsMa$i_min" ["mso4_guan"]="MsGu$i_min" ["mso4_imim"]="MsIm$i_min" ["mso4_mamm"]="MsMa$i_min" )

    for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
    do
        echo s/xxx_i_min_xxx/${i_min}/g > ./tmp
        echo s/xxx_i_max_xxx/${i_max}/g >> ./tmp
        echo s/xxx_pair_xxx/${pair}/g >> ./tmp
        echo s/xxx_name_xxx/${names[$pair]}/g >> ./tmp
        sed -f ./tmp ./template_job_get_energies.qs > job_get_energies_${pair}_${i_min}.qs
        rm ./tmp
    done

done



