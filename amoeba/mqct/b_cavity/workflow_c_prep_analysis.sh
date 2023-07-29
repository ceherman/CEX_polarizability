#!/bin/bash

for ion in acet esna mso4 guan imim mamm
do
    cd $ion

    cp ../analyze_sepdcd.py .
    cp ../mywallfunction.py .
    cp ../input .
    cp ../process_seven_point_openmm.py .
    cp ../7p_integral.py .
    cp ../runme_analyze.qs .

    cd ../
done
