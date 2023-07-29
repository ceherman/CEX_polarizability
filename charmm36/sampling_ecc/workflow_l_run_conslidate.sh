#!/bin/bash

for anion in acet esna mso4
do
    for cation in guan imim mamm
    do
		sbatch job_consolidate_${anion}_${cation}.qs
    done
done
