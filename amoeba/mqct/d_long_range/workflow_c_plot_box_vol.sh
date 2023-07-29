#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    ln -sf ../plot_box_volume.py .
    python plot_box_volume.py $ion

    cd ../
done
