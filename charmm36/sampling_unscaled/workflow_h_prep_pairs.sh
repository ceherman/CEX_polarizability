#!/bin/bash

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
        cd ${anion}_${cation}
        for i in {1..22}
        do
            for j in {23..44}
            do
                new_dir=pair_${i}_${j}
                cd $new_dir
                # cp ../../pair.namd .
				# cp ../../job_get_energies.qs .
                cd ../
            done
        done
        cd ../
    done
done
