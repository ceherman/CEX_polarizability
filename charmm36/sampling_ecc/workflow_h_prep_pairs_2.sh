#!/bin/bash

for pair in acet_imim acet_mamm esna_guan esna_imim
do
    cd ${pair}
    for i in {1..22}
    do
        for j in {23..44}
        do
            new_dir=pair_${i}_${j}
            cd $new_dir
            cp ../../pair_pme_off_2.namd .
            cd ../
        done
    done
    cd ../
done
