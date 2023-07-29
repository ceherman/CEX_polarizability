#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    ln -sf ../plot_gaussian_check.py .
    python plot_gaussian_check.py $ion

    cd ../
done
