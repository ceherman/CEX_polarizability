#!/bin/bash

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
		echo s/xxx_anion_xxx/${anion}/g > tmp
        echo s/xxx_cation_xxx/${cation}/g >> tmp
        sed -f tmp template_consolidate_pairwise_pme_off.qs > job_consolidate_${anion}_${cation}.qs
		rm tmp
    done
done
