#!/bin/bash

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
        for i_anion in {1..22}
        do
            sbatch job_get_energies_${anion}_${cation}_${i_anion}.qs
        done
    done
done

