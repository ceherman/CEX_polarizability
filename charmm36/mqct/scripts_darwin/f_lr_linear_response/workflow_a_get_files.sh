#!/bin/bash

previous_radius=4.9745550
radius_rounded=$(echo $previous_radius | awk '{printf "%.4f", $1}') # 4 decimal float
base_name=wbigbox_${radius_rounded}
new_radius=$(echo $previous_radius | awk '{print int($1+0.5)}').0 # nearest whole number

for ion in acet esna mso4 guan imim mamm
do
    mkdir -p $ion
    cd $ion

    base_path=../../../mqct_for_summit_tip/b_chemistry_with_charges/${ion}
    cp ${base_path}/${base_name}.coor ./
    cp ${base_path}/${base_name}.restart.coor ./
    cp ${base_path}/${base_name}.restart.vel ./
    cp ${base_path}/${base_name}.restart.xsc ./
    cp ${base_path}/system.psf ./
    cp ${base_path}/residuebased.zero.tcl ./

    echo s/xx_previous_radius_xx/${previous_radius}/g > ./tmp
    echo s/xx_new_radius_xx/${new_radius}/g >> ./tmp
    echo s/xx_job_id_xx/long_range/g >> ./tmp
    echo s/xx_base_name_xx/${base_name}/g >> ./tmp
    echo s/xxx_ion_xxx/${ion}/g >> ./tmp

    sed -f ./tmp ../files/long_range_template.namd > ./long_range.namd
    sed -f ./tmp ../files/get_energy_template.namd > ./get_energy.namd
    sed -f ./tmp ../files/runme_long_range.qs > ./runme_long_range.qs
    sed -f ./tmp ../files/runme_get_energy.qs > ./runme_get_energy.qs
    # cp ../files/runme_get_energy_local.sh .
    rm ./tmp

    cd ../
done
