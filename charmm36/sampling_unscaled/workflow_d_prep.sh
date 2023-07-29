#!/bin/bash

i=1
first_ts=0
run=50000000 
# (0, 500000), (0, 75000000), (75000000, x), etc.

declare -A names
names=( ["acet_guan"]="AcGu$i" ["acet_imim"]="AcIm$i" ["acet_mamm"]="AcMa$i" ["esna_guan"]="EsGu$i" ["esna_imim"]="EsIm$i" ["esna_mamm"]="EsMa$i" ["mso4_guan"]="MsGu$i" ["mso4_imim"]="MsIm$i" ["mso4_mamm"]="MsMa$i" )

let i_prev=$i-1

for pair in acet_guan acet_imim acet_mamm esna_guan esna_imim esna_mamm mso4_guan mso4_imim mso4_mamm
do
    cd $pair

    echo s/xxx_i_xxx/${i}/g > ./prep
    echo s/xxx_i_prev_xxx/${i_prev}/g >> ./prep
    echo s/xxx_first_ts_xxx/${first_ts}/g >> ./prep
    echo s/xxx_run_xxx/${run}/g >> ./prep
	echo s/xxx_job_name_xxx/${names[$pair]}/g >> ./prep

    sed -f ./prep ../sampling_template.namd > sampling_${i}.namd
    sed -f ./prep ../job_template.qs > job_${i}.qs
    # rm prep

    cd ../
done


