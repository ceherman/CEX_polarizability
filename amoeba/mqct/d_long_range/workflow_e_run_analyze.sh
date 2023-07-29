#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    sbatch runme_analyze_all.qs
    sbatch runme_analyze_water.qs

    cd ../
done
