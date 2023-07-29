#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

	ln -sf ../make_arc_file.py .
	ln -sf ../manipulate_txyz_ceh.py .
    cp ../analyze .
    cp ../amoebabio18_mod.prm .
    ln -sf ../extract_frame_energies.py .

    echo s/xxx_ion_xxx/${ion}/g > ./prep
    sed -f ./prep ../runme_analyze_all.qs > runme_analyze_all.qs
    sed -f ./prep ../runme_analyze_water.qs > runme_analyze_water.qs
    rm ./prep

    cd ../
done
