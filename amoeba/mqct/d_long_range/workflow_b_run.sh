#!/bin/bash

for ion in acet esna mso4 guan imim # mamm
do
    cd $ion
    sbatch runme.qs
    cd ../
done
