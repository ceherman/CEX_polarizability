#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    cp ../chemistry.py .
    cp ../dcdsubsetfile.py .
    cp ../dcdsubsetreporter.py .

    echo s/xxx_ion_xxx/${ion}/g > ./prep
    sed -f ./prep ../runme.qs > runme.qs
    rm ./prep

    cd ../
done
